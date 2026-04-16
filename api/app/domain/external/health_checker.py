#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/20 1:18
@Author  : shentuk@outlook.com
@File    : health_checker.py
"""
from typing import Protocol

from app.domain.models.health_status import HealthStatus


class HealthChecker(Protocol):
    """服务健康检查协议"""

    async def check(self) -> HealthStatus:
        """用于检查对应的服务是否健康"""
        ...
