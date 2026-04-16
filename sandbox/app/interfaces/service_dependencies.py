#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/05/10 17:21
@Author  : shentuk@outlook.com
@File    : service_dependencies.py
"""
from functools import lru_cache

from app.services.file import FileService
from app.services.shell import ShellService
from app.services.supervisor import SupervisorService


@lru_cache()
def get_shell_service() -> ShellService:
    return ShellService()


@lru_cache()
def get_file_service() -> FileService:
    return FileService()


@lru_cache()
def get_supervisor_service() -> SupervisorService:
    return SupervisorService()
