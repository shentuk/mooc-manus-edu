#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/05/18 1:44
@Author  : shentuk@outlook.com
@File    : json_parser.py
"""
from typing import Protocol, Optional, Any, Union, Dict, List


class JSONParser(Protocol):
    """JSON解析器，用于解析json字符串并修复"""

    async def invoke(self, text: str, default_value: Optional[Any] = None) -> Union[Dict, List, Any]:
        """调用函数，用于将传递进来的文本进行解析并返回"""
        ...
