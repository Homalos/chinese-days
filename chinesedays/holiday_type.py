#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: chinese-days
@FileName   : holiday_type.py
@Date       : 2025/9/30 09:42
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 节假日类型枚举
Holiday type enumeration
"""
from enum import Enum


class HolidayType(Enum):
    # 法定节假日
    # Public holidays
    LEGAL = "legal"
    # 作日(含调休工作日，将原休息日置换为工作日)
    # Workdays (including adjusted workdays, where a regular day off is replaced with a workday)
    WORK = "work"
    # 补休日
    # Compensatory day off
    IN_LIEU = "in_lieu"
