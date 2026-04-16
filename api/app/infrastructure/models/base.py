#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/18 10:45
@Author  : shentuk@outlook.com
@File    : base.py
"""
from sqlalchemy.orm import declarative_base

# 定义基础ORM类，让所有模型都继承这个类
Base = declarative_base()
