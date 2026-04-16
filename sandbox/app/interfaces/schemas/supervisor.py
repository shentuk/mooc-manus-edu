#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/05/26 1:52
@Author  : shentuk@outlook.com
@File    : supervisor.py
"""
from typing import Optional

from pydantic import BaseModel, Field


class TimeoutRequest(BaseModel):
    """激活超时销毁请求"""
    minutes: Optional[int] = Field(default=None, description="分钟数")
