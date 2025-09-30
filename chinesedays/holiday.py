#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: chinese-days
@FileName   : holiday.py
@Date       : 2025/9/30 13:55
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 节假日对象类
"""
from datetime import datetime, date


class Holiday:

    def __init__(self, date_str: str, chinese_name: str, english_name: str, holiday_type: str):
        """
        初始化节假日对象

        Args:
            date_str: 日期字符串，格式为 'YYYY-MM-DD'
            chinese_name: 中文名称
            english_name: 英文名称
            holiday_type: 节假日类型
        """
        self.date_str = date_str
        self.chinese_name = chinese_name
        self.english_name = english_name
        self.holiday_type = holiday_type
        self._date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    @property
    def name(self) -> str:
        """获取中文名称"""
        return self.chinese_name

    @property
    def date(self) -> date:
        """获取日期对象"""
        return self._date_obj

    @property
    def year(self) -> int:
        """获取年份"""
        return self._date_obj.year

    @property
    def month(self) -> int:
        """获取月份"""
        return self._date_obj.month

    @property
    def day(self) -> int:
        """获取日期"""
        return self._date_obj.day

    def __str__(self) -> str:
        return f"{self.date_str} {self.chinese_name}"

    def __repr__(self) -> str:
        return f"Holiday('{self.date_str}', '{self.chinese_name}', '{self.english_name}', '{self.holiday_type}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Holiday):
            return False
        return self.date_str == other.date_str

    def __lt__(self, other) -> bool:
        if not isinstance(other, Holiday):
            return NotImplemented
        return self._date_obj < other._date_obj
