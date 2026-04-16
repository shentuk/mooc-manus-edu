#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/14 10:46
@Author  : shentuk@outlook.com
@File    : main.py
"""
import asyncio
import logging
import traceback
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.logging import setup_logging
from app.infrastructure.storage.cos import get_cos
from app.infrastructure.storage.postgres import get_postgres
from app.infrastructure.storage.redis import get_redis
from app.interfaces.endpoints.routes import router
from app.interfaces.errors.exception_handlers import register_exception_handlers
from app.interfaces.service_dependencies import get_agent_service
from core.config import get_settings

# 1.加载配置信息
settings = get_settings()

# 2.初始化日志系统
setup_logging()
logger = logging.getLogger()

# 3.定义FastAPI路由tags标签
openapi_tags = [
    {
        "name": "状态模块",
        "description": "包含 **状态监测** 等API 接口，用于监测系统的运行状态。"
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """创建FastAPI应用生命周期上下文管理器"""
    # 0.重新初始化日志系统(uvicorn启动时dictConfig会影响根日志处理器，需要在此重新配置)
    setup_logging()

    # 1.日志打印代码已经开始执行了
    logger.info("EduManus 教学智能体正在初始化")

    try:
        # 2.运行数据库迁移(将数据同步到生产环境)
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

        # 3.初始化Redis/Postgres/Cos客户端
        await get_redis().init()
        await get_postgres().init()
        await get_cos().init()
    except Exception as e:
        logger.exception("EduManus 启动失败: %s", e)
        raise

    try:
        # 4.lifespan分界点
        yield
    finally:
        try:
            # 5.等待agent服务关闭
            logger.info("EduManus 教学智能体正在关闭")
            await asyncio.wait_for(get_agent_service().shutdown(), timeout=30.0)
            logger.info("Agent服务成功关闭")
        except asyncio.TimeoutError:
            logger.warning("Agent服务关闭超时, 强制关闭, 部分任务将被释放")
        except Exception as e:
            logger.error(f"Agent服务关闭期间出现错误: {str(e)}")

        # 6.关闭其他应用
        await get_redis().shutdown()
        await get_postgres().shutdown()
        await get_cos().shutdown()

        logger.info("EduManus 应用关闭成功")


# 4.创建EduManus应用实例
app = FastAPI(
    title="EduManus 教学智能体",
    description="EduManus 是一个面向教学领域的多智能体协作系统，基于 Planner + ReAct 架构，支持课程规划、作业批改、答疑辅导、学习分析和试题生成等教学场景，可通过 A2A+MCP 连接外部教学Agent和工具",
    lifespan=lifespan,
    openapi_tags=openapi_tags,
    version="1.0.0",
)

# 5.配置CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6.注册错误处理器
register_exception_handlers(app)

# 7.集成路由
app.include_router(router, prefix="/api")