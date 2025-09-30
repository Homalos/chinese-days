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
"""
from enum import Enum


class HolidayType(Enum):
    LEGAL = "legal"     # 法定节假日
    WORK = "work"       # 工作日(含调休工作日，将原休息日置换为工作日)
    IN_LIEU = "in_lieu" # 补休日
