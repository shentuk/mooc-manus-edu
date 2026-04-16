#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/17 10:48
@Author  : shentuk@outlook.com
@File    : app_config_repository.py
"""
from typing import Protocol, Optional

from app.domain.models.app_config import AppConfig


class AppConfigRepository(Protocol):
    """应用配置仓库"""

    def load(self) -> Optional[AppConfig]:
        """加载获取应用配置"""
        ...

    def save(self, app_config: AppConfig) -> None:
        """存储更新的应用配置"""
        ...
