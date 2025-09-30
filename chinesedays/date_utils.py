#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: chinese-days
@FileName   : date_utils.py
@Date       : 2025/9/30 09:32
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 中国节假日、工作日查询工具便捷函数

更多详细用法参考：examples/usage_examples.py
完整测试用例参考：tests/test_days.py

A convenient tool for querying Chinese holidays and working days

For more detailed usage examples, see: examples/usage_examples.py
For complete test cases, see: tests/test_days.py
"""
from datetime import datetime, date
from typing import Union, Optional, Iterable

from chinesedays.days_base import DaysBase
from chinesedays.holiday import Holiday
from chinesedays.holiday_type import HolidayType

# Singleton instance
_chinese_days = DaysBase()


def convert_str_to_datetime(y_m_d_str: str) -> datetime:
    """
    字符串年月日转换为日期对象

    Convert a string representing a date (YYYY-MM-DD) to a datetime object

    Args:
        y_m_d_str: 2024-05-23

    Returns:
        datetime: 日期对象
        datetime object
    """
    return _chinese_days.convert_str_to_datetime(y_m_d_str)

def convert_date_obj_to_str(date_obj: datetime) -> str:
    """
    日期对象转换为字符串格式

    Convert the object to a string format.

    Args:
        date_obj: 2024-05-23

    Returns:
        str: 2024-05-23
    """
    return _chinese_days.convert_date_obj_to_str(date_obj)

def get_day_of_week(date_input: Union[datetime, date, str, int]) -> int:
    """
    获取日期是星期几

    Get the day of the week for that date.

    Args:
        date_input: 日期对象，例如 2024-01-01
        Date object, for example, 2024-01-01

    Returns:
        int: 0、1、2、3、4、5、6，从0开始
        0, 1, 2, 3, 4, 5, 6; starting from 0
    """
    return _chinese_days.get_day_of_week(date_input)


def is_workday(date_input: Union[datetime, date, str, int]) -> bool:
    """
    判断是否为工作日

    Determine if it is a working day.

    Args:
        date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        supports datetime, date, or 'YYYY-MM-DD' string format

    Returns:
        bool: 是否为工作日
        Is it a working day?
    """
    return _chinese_days.is_workday(date_input)

def is_holiday(date_input: Union[datetime, date, str, int]) -> bool:
    """
    判断是否为节假日

    Determine if it is a holiday or not.

    Args:
        date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Supports datetime, date, or 'YYYY-MM-DD' format string

    Returns:
        bool: 是否为节假日
        Is it a holiday?
    """
    return _chinese_days.is_holiday(date_input)

def is_weekend(date_input: Union[datetime, date, str, int]) -> bool:
    """
    判断是否为周末

    Determine if it is the weekend.

    Args:
        date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Supports datetime, date, or 'YYYY-MM-DD' format string

    Returns:
        bool: 是否为周末
        Is it the weekend?
    """
    return _chinese_days.is_weekend(date_input)

def get_holidays(years: Optional[Union[int, Iterable[int]]] = None) -> list[Holiday]:
    """
    获取指定年份的节假日列表

    Get the list of holidays for a specific year

    Args:
        years: 年，可以是单个整数或迭代器，如[2023, 2024]。如果为None，返回所有年份的节假日
        The year parameter can be a single integer or an iterable (e.g., [2023, 2024]).
        If set to None, it will return holidays for all years.

    Returns:
        list[Holiday]: 指定年份的节假日对象列表，按日期排序
        A list of holiday objects for the specified year, sorted by date.
    """
    # 处理年份参数(Process the year parameter)
    if years is None:
        # 如果没有指定年份，返回所有年份的节假日
        # If no year is specified, return the list of holidays for all years.
        target_years = set()
        for date_str in _chinese_days.get_holiday_details().keys():
            year = int(date_str.split('-')[0])
            target_years.add(year)
    elif isinstance(years, int):
        # 单个年份(single year)
        target_years = {years}
    else:
        # 多个年份的迭代器(Iterator for multiple years)
        target_years = set(years)
    
    # 收集指定年份的节假日
    # Collect holiday dates for a specific year
    holidays = []
    for date_str, detail in _chinese_days.get_holiday_details().items():
        year = int(date_str.split('-')[0])
        if year in target_years:
            # 解析节假日详细信息，格式：'English Name,中文名,类型'
            # Analyze holiday details，Format: 'English Name, Chinese Name, Type'
            parts = detail.split(',')
            english_name = parts[0] if len(parts) > 0 else ""
            chinese_name = parts[1] if len(parts) > 1 else ""
            holiday_type = parts[2] if len(parts) > 2 else ""
            
            # 创建Holiday对象(Create a Holiday object)
            holiday_obj = Holiday(date_str, chinese_name, english_name, holiday_type)
            holidays.append(holiday_obj)
    
    holidays.sort()
    return holidays
    
def get_holiday_type(date_input: Union[datetime, date, str, int]) -> Optional[HolidayType]:
    """
    获取节假日类型

    Get holiday type information

    Args:
        date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Supports datetime, date, or 'YYYY-MM-DD' format string

    Returns:
        HolidayType: 节假日类型，如果不是特殊日期则返回None
        Holiday type; returns None if not a special date.
    """
    return _chinese_days.get_holiday_type(date_input)

def get_holiday_name(date_input: Union[datetime, date, str, int]) -> Optional[str]:
    """
    获取节假日名称

    Get the names of holidays

    Args:
        date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Supports datetime, date, or 'YYYY-MM-DD' format string

    Returns:
        str: 节假日名称，如果不是节假日则返回None
        Holiday name; returns "None" if it is not a holiday.
    """
    return _chinese_days.get_holiday_name(date_input)


def get_workdays_in_range(start_date: Union[datetime, date, str, int],
                         end_date: Union[datetime, date, str, int],
                         include_weekends: bool = True) -> list[date]:
    """
    获取日期范围内的所有工作日

    Get all working days within the specified date range.

    Args:
        start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Start date; supports datetime, date, or 'YYYY-MM-DD' format string
        end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        End date; supports datetime, date, or 'YYYY-MM-DD' format string
        include_weekends: 是否包含周末的调休工作日，默认True
        Whether to include adjusted working days that fall on weekends; default value is True.

    Returns:
        list: 日期范围内的所有工作日列表
        List of all working days within the specified date range
    """
    return _chinese_days.get_workdays_in_range(start_date, end_date, include_weekends)

def get_holidays_in_range(start_date: Union[datetime, date, str, int],
                         end_date: Union[datetime, date, str, int],
                         include_weekends: bool = True) -> list[date]:
    """
    获取日期范围内的所有节假日

    Get all holidays within the specified date range.

    Args:
        start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Start date; supports datetime, date, or 'YYYY-MM-DD' format string
        end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        End date; supports datetime, date, or 'YYYY-MM-DD' format string
        include_weekends: 是否包含普通周末，默认True
        Whether to include adjusted working days that fall on weekends; default value is True.

    Returns:
        list: 日期范围内的所有节假日列表
        List of all holidays within the specified date range
    """
    return _chinese_days.get_holidays_in_range(start_date, end_date, include_weekends)

def find_next_workday(date_input: Union[datetime, date, str, int],
                     delta_days: int = 1) -> date:
    """
    查找下N个工作日

    Find the next N working days

    Args:
        date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Supports datetime, date, or 'YYYY-MM-DD' format string
        delta_days: 要找的第几个工作日（正数向前，负数向后）
        Enter the number of the desired workday (positive numbers move forward, negative numbers move backward).

    Returns:
        date: 目标工作日
        Target working days
    """
    return _chinese_days.find_next_workday(date_input, delta_days)

def count_workdays(start_date: Union[datetime, date, str, int],
                  end_date: Union[datetime, date, str, int],
                  include_weekends: bool = True) -> int:
    """
    计算日期范围内的工作日数量

    Calculate the number of working days within a given date range.

    Args:
        start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Start date; supports datetime, date, or 'YYYY-MM-DD' format string
        end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        End date; supports datetime, date, or 'YYYY-MM-DD' format string
        include_weekends: 是否包含周末的调休工作日，默认True
        Whether to include adjusted working days that fall on weekends; default value is True.

    Returns:
        int: 日期范围内的工作日数量
        Number of working days within the date range
    """
    return len(get_workdays_in_range(start_date, end_date, include_weekends))


def count_holidays(start_date: Union[datetime, date, str, int],
                       end_date: Union[datetime, date, str, int],
                       include_weekends: bool = True) -> int:
    """
    计算日期范围内的节假日数量

    Calculate the number of holidays within the specified date range.

    Args:
        start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        Start date; supports datetime, date, or 'YYYY-MM-DD' format string
        end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
        End date; supports datetime, date, or 'YYYY-MM-DD' format string
        include_weekends: 是否包含普通周末，默认True
        Whether to include adjusted working days that fall on weekends; default value is True.

    Returns:
        int: 日期范围内的节假日数量
        Number of holidays within the date range
    """
    return len(get_holidays_in_range(start_date, end_date, include_weekends))
