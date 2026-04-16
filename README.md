# EduManus - 教学领域多智能体协作系统

EduManus 是基于 MoocManus 定制的**教学领域多智能体协作系统**。它将通用 AI Agent 能力聚焦于教育教学场景，为教师提供课程规划、作业批改、答疑辅导、学习分析、试题生成等智能化教学辅助服务。

系统支持完全私有化部署，使用 A2A（Agent-to-Agent）+ MCP（Model Context Protocol）协议连接外部智能体和工具，同时支持在沙箱中安全运行代码和操作。

---

## ✨ 功能特性

### 🎓 教学专用智能体
- **课程规划**：根据学科、年级、教学目标自动生成课程大纲和教学计划
- **作业批改**：智能批改学生作业，提供详细评分和个性化反馈
- **答疑辅导**：基于知识点进行因材施教的答疑解惑
- **学习分析**：分析学生学习数据，生成可视化报告和改进建议

### 🛠️ 5 个教学专用工具
| 工具 | 功能 | 参数 |
|------|------|------|
| `edu_create_course_outline` | 课程大纲生成 | 学科、年级、教学目标、课时 |
| `edu_grade_assignment` | 作业批改与评分 | 学生答案、参考答案、评分标准 |
| `edu_generate_quiz` | 测验题目生成 | 知识点、题型（6种）、难度（3级） |
| `edu_analyze_learning` | 学习数据分析 | 学习数据、分析类型（4种） |
| `edu_create_lesson_plan` | 教案创建 | 课题、教学方法、学生水平 |

### 🎨 教学化 UI 界面
- 教学场景欢迎语和推荐问题
- EduManus 品牌标识（蓝绿渐变教育主题）
- 教学任务导向的交互设计

### 🔌 协议扩展
- **A2A 协议**：连接远程教学智能体（如学科辅导 Agent、批改 Agent）
- **MCP 协议**：集成外部教学工具（如题库检索、知识图谱查询、课程平台对接）

### 🐳 Docker 一键部署
- 完整的 Docker Compose 编排
- 包含 API、UI、数据库、缓存、沙箱、网关全套服务

---

## 🚀 快速部署

### 环境要求

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **内存** >= 4GB（推荐 8GB）
- **磁盘** >= 10GB

### 部署步骤

#### 1. 克隆项目

```bash
git clone <your-repo-url> mooc-manus-edu
cd mooc-manus-edu
```

#### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（必须修改的项）
vim .env
```

**必须配置的项目：**

```bash
# 腾讯云 COS 文件存储（用于教学资料上传）
COS_SECRET_ID=your_cos_secret_id_here
COS_SECRET_KEY=your_cos_secret_key_here
COS_BUCKET=your_cos_bucket_here
```

#### 3. 配置 AI 模型

编辑 `api/config.yaml` 中的 LLM 配置：

```yaml
llm_config:
  base_url: https://api.deepseek.com/    # 模型提供商地址（兼容 OpenAI 格式）
  api_key: your_api_key_here              # API 密钥
  model_name: deepseek-reasoner           # 模型名称（需支持工具调用）
  temperature: 0.7
  max_tokens: 8192
```

> 💡 也可以在部署后通过 UI 的「设置」页面在线修改模型配置。

#### 4. 启动所有服务

```bash
docker compose up -d --build
```

#### 5. 访问系统

打开浏览器访问：`http://your-server-ip:8088`

---

## 📚 教学场景使用说明

### 典型使用场景

| 场景 | 示例输入 | 系统能力 |
|------|---------|---------|
| **课程规划** | "帮我制定一份 Python 编程入门课程大纲，面向大一学生，共 16 课时" | 生成结构化课程大纲，包含教学目标、知识点、课时安排 |
| **作业批改** | "批改这份数学作业并给出详细反馈"（附上作业图片/文件） | 逐题批改、评分、错误分析、改进建议 |
| **试题生成** | "根据'牛顿运动定律'知识点生成一套练习题，包含选择题和计算题" | 按知识点、题型、难度生成试题及参考答案 |
| **学习分析** | "分析班级学生的期中考试成绩数据并生成报告" | 成绩分布、薄弱知识点、学生分层、改进建议 |
| **教案制作** | "为'光合作用'课题创建一份教案，采用探究式教学法" | 标准格式教案，包含教学环节、时间分配、活动设计 |

### 进阶用法

- **上传文件**：支持上传学生作业、成绩表格等文件进行分析
- **连续对话**：在同一会话中持续优化教学方案
- **MCP 扩展**：通过设置页面添加外部教学工具服务器
- **A2A 协作**：连接专业学科辅导 Agent 进行协同教学

---

## 📁 项目结构

```
mooc-manus-edu/
├── api/                    # 后端 API 服务（FastAPI）
│   ├── app/
│   │   ├── domain/
│   │   │   └── services/
│   │   │       ├── flows/          # 智能体工作流
│   │   │       ├── prompts/        # 系统提示词（中文/英文）
│   │   │       └── tools/          # 工具集（含教学工具）
│   │   │           └── education.py  # 教学专用工具
│   │   └── main.py
│   ├── config.yaml         # 后端配置（LLM、教学参数）
│   └── Dockerfile
├── ui/                     # 前端服务（Next.js）
│   ├── src/
│   │   ├── app/            # 页面（首页、会话详情）
│   │   ├── components/     # 组件（教学化 UI）
│   │   └── config/         # 前端配置（推荐问题等）
│   └── Dockerfile
├── sandbox/                # 沙箱服务（Ubuntu + Chrome + VNC）
│   └── Dockerfile
├── nginx/                  # Nginx 网关配置
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
├── docs/                   # 文档
│   └── system_design.md    # 系统设计文档
├── docker-compose.yml      # Docker 编排配置
├── .env.example            # 环境变量模板
└── README.md               # 本文件
```

---

## ⚙️ 配置说明

### config.yaml（后端配置）

| 配置段 | 说明 |
|--------|------|
| `llm_config` | LLM 模型配置（base_url、api_key、model_name、temperature、max_tokens） |
| `agent_config` | 智能体配置（最大迭代次数、重试次数、搜索结果数） |
| `edu_config` | 教学配置（工具开关、知识库路径、题库路径、默认学科/年级） |
| `mcp_config` | MCP 服务器配置（外部工具集成） |
| `a2a_config` | A2A 远程智能体配置 |

### 环境变量（.env）

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `COS_SECRET_ID` | ✅ | - | 腾讯云 COS SecretId |
| `COS_SECRET_KEY` | ✅ | - | 腾讯云 COS SecretKey |
| `COS_BUCKET` | ✅ | - | COS 存储桶名称 |
| `POSTGRES_USER` | ❌ | postgres | 数据库用户名 |
| `POSTGRES_PASSWORD` | ❌ | postgres | 数据库密码 |
| `POSTGRES_DB` | ❌ | edumanus | 数据库名称 |
| `NGINX_PORT` | ❌ | 8088 | 对外访问端口 |
| `LOG_LEVEL` | ❌ | INFO | 日志级别 |

---

## 🏗️ 服务架构

```
                    ┌──────────────────┐
     Port 8088      │  Nginx Gateway   │
   ─────────────────►  (edumanus-nginx)│
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │ /                       │ /api
                ▼                         ▼
         ┌──────────────┐        ┌───────────────┐
         │  Next.js UI  │        │  FastAPI API   │
         │(edumanus-ui) │        │(edumanus-api)  │
         │  Port 3000   │        │  Port 8000     │
         └──────────────┘        └───────┬────────┘
                                         │
                      ┌──────────────────┼──────────────────┐
                      │                  │                   │
                      ▼                  ▼                   ▼
               ┌────────────┐    ┌────────────┐     ┌──────────────┐
               │ PostgreSQL │    │   Redis    │     │   Sandbox    │
               │(edumanus-  │    │(edumanus-  │     │(edumanus-    │
               │ postgres)  │    │ redis)     │     │ sandbox)     │
               └────────────┘    └────────────┘     └──────────────┘
```

### 容器列表

| 容器名称 | 服务 | 说明 |
|---------|------|------|
| edumanus-nginx | Nginx | 反向代理网关，唯一对外暴露端口 |
| edumanus-ui | Next.js | 教学化前端 UI 服务 |
| edumanus-api | FastAPI | 教学智能体后端 API 服务 |
| edumanus-postgres | PostgreSQL | 数据库（会话、配置持久化） |
| edumanus-redis | Redis | 缓存（会话状态、消息队列） |
| edumanus-sandbox | Sandbox | 沙箱环境（Chrome + VNC，代码执行） |

---

## 🔧 常用命令

```bash
# 启动所有服务（后台运行）
docker compose up -d --build

# 查看所有服务状态
docker compose ps

# 查看服务日志
docker compose logs -f                  # 所有服务
docker compose logs -f edumanus-api     # 仅 API 服务
docker compose logs -f edumanus-ui      # 仅 UI 服务

# 重启单个服务
docker compose restart edumanus-api

# 停止所有服务
docker compose down

# 停止并清除数据卷（⚠️ 谨慎操作，会删除所有数据）
docker compose down -v
```

---

## 🔒 启用 HTTPS

1. 将 SSL 证书放入 `nginx/ssl/` 目录：
   - `fullchain.pem`（证书链）
   - `privkey.pem`（私钥）

2. 修改 `nginx/conf.d/default.conf`，取消 SSL server 块注释

3. 修改 `docker-compose.yml`，取消 443 端口映射注释

4. 重启 Nginx：
   ```bash
   docker compose restart edumanus-nginx
   ```

---

## 📖 本地开发

各子项目的本地开发说明请参考对应目录下的 README：

- [API 服务](./api/README.md)
- [前端 UI](./ui/README.md)
- [沙箱服务](./sandbox/README.md)

---

## 📄 许可证

本项目基于 MoocManus 开源项目定制开发，仅用于教学研究目的。
