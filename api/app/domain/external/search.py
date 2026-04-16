#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/05/24 14:55
@Author  : shentuk@outlook.com
@File    : search.py
"""
from typing import Protocol, Optional

from app.domain.models.search import SearchResults
from app.domain.models.tool_result import ToolResult


class SearchEngine(Protocol):
    """搜索引擎API接口协议"""

    async def invoke(self, query: str, date_range: Optional[str] = None) -> ToolResult[SearchResults]:
        """调用搜索引擎并传递query+date_range(日期检索范围)调用搜索引擎获取数据"""
        ...
