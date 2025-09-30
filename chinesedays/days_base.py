#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: chinese-days
@FileName   : days_base.py
@Date       : 2025/9/30 09:46
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 中国节假日、工作日查询库

更多详细用法参考：examples/usage_examples.py
完整测试用例参考：tests/test_days.py

Chinese Public Holidays and Working Days Database

For more detailed usage examples, please refer to: examples/usage_examples.py
For complete test cases, please refer to: tests/test_days.py
"""
import json
import logging
import re
from datetime import datetime, date, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Union, Optional

from chinesedays.holiday_type import HolidayType

logger = logging.getLogger(__name__)


class DaysBase:

    _instance = None
    _data_loaded = False

    def __new__(cls) -> 'DaysBase':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        if not self._data_loaded:
            self._holidays: set[str] = set()
            self._workdays: set[str] = set()
            self._in_lieu_days: set[str] = set()
            self._holiday_details: dict[str, str] = {}
            self._workday_details: dict[str, str] = {}
            self._load_data()
            self._data_loaded = True

    def _load_data(self) -> None:
        try:
            possible_paths = [
                # 开发环境路径
                Path(__file__).parent.parent / "data" / "chinese-days.json",
                # 打包后的路径
                Path(__file__).parent / "data" / "chinese-days.json",
                # 当前工作目录
                Path("data/chinese-days.json")
            ]

            data_file = None
            for path in possible_paths:
                if path.exists():
                    data_file = path
                    break

            if not data_file:
                raise FileNotFoundError("Unable to find the data file chinese-days.json")

            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 转换为集合以提高查找性能
            holidays = data.get('holidays', {})
            workdays = data.get('workdays', {})
            in_lieu_days = data.get('inLieuDays', {})

            self._holidays = set(holidays.keys())
            self._workdays = set(workdays.keys())
            self._in_lieu_days = set(in_lieu_days.keys())

            # 保存详细信息用于查询
            self._holiday_details = holidays
            self._workday_details = workdays

        except Exception as e:
            logger.error(f"An error occurred while loading the data file: {e}")
            raise

    def get_holiday_details(self) -> dict[str, str]:
        """
        获取节假日详细信息
        Returns:
            dict: 节假日详细信息
        """
        return self._holiday_details

    @lru_cache(maxsize=1000)
    def is_workday(self, date_input: Union[datetime, date, str, int]) -> bool:
        """
        判断是否为工作日

        Args:
            date_input: 日期，支持 datetime、date、'YYYY-MM-DD' 或 YYYY-MM-DD 格式字符串

        Returns:
            bool: 是否为工作日
        """
        date_str = self._normalize_date(date_input)
        dt = self._parse_date(date_input)

        # 如果在调休工作日列表中，直接返回True
        if date_str in self._workdays:
            return True

        # 如果在节假日列表中，直接返回False
        if date_str in self._holidays:
            return False

        # 否则按照常规逻辑：周一到周五为工作日
        weekday = dt.isoweekday()  # Monday=1, Sunday=7
        return 1 <= weekday <= 5

    @lru_cache(maxsize=1000)
    def is_holiday(self, date_input: Union[datetime, date, str, int]) -> bool:
        """
        判断是否为节假日

        Args:
            date_input: 日期，支持 datetime、date、'YYYY-MM-DD' 或 YYYY-MM-DD 格式字符串

        Returns:
            bool: 是否为节假日
        """
        return not self.is_workday(date_input)

    def is_weekend(self, date_input: Union[datetime, date, str, int]) -> bool:
        """
        判断是否为周末

        Args:
            date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串

        Returns:
            bool: 是否为周末
        """
        dt = self._parse_date(date_input)
        return dt.isoweekday() in [6, 7]

    def get_holiday_type(self, date_input: Union[datetime, date, str, int]) -> Optional[HolidayType]:
        """
        获取节假日类型

        Args:
        date_input: 日期，支持 datetime、date、'YYYY-MM-DD' 或 YYYY-MM-DD 格式字符串

        Returns:
            HolidayType: 节假日类型，如果不是特殊日期则返回None
        """
        date_str = self._normalize_date(date_input)

        if date_str in self._holidays:
            return HolidayType.LEGAL
        elif date_str in self._workdays:
            return HolidayType.WORK
        elif date_str in self._in_lieu_days:
            return HolidayType.IN_LIEU
        else:
            return None

    def get_holiday_name(self, date_input: Union[datetime, date, str, int]) -> Optional[str]:
        """
        获取节假日名称

        Args:
            date_input: 日期，支持 datetime、date、'YYYY-MM-DD' 或 YYYY-MM-DD 格式字符串

        Returns:
            str: 节假日名称，如果不是节假日则返回None
        """
        date_str = self._normalize_date(date_input)

        if date_str in self._holiday_details:
            # 解析格式：'English Name,中文名,类型'
            detail = self._holiday_details[date_str]
            parts = detail.split(',')
            return parts[1] if len(parts) > 1 else parts[0]

        return None

    def get_workdays_in_range(self, start_date: Union[datetime, date, str, int],
                              end_date: Union[datetime, date, str, int],
                              include_weekends: bool = True) -> list[date]:
        """
        获取日期范围内的所有工作日

        Args:
            start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            include_weekends: 是否包含周末的调休工作日，默认True

        Returns:
            list: 日期范围内的所有工作日列表
        """
        start = self._parse_date(start_date)
        end = self._parse_date(end_date)

        workdays = []
        current = start

        while current <= end:
            if self.is_workday(current):
                # 如果include_weekends为False，则排除周末的调休工作日
                if include_weekends or (1 <= current.isoweekday() <= 5):
                    workdays.append(current.date() if isinstance(current, datetime) else current)
            current += timedelta(days=1)

        return workdays

    def get_holidays_in_range(self, start_date: Union[datetime, date, str, int],
                              end_date: Union[datetime, date, str, int],
                              include_weekends: bool = True) -> list[date]:
        """
        获取日期范围内的所有节假日

        Args:
            start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            include_weekends: 是否包含普通周末，默认True

        Returns:
            list: 日期范围内的所有节假日列表
        """
        start = self._parse_date(start_date)
        end = self._parse_date(end_date)

        holidays = []
        current = start

        while current <= end:
            if self.is_holiday(current):
                # 如果include_weekends为False，则排除普通周末
                if include_weekends or (1 <= current.isoweekday() <= 5):
                    holidays.append(current.date() if isinstance(current, datetime) else current)
            current += timedelta(days=1)

        return holidays

    def find_next_workday(self, date_input: Union[datetime, date, str, int],
                          delta_days: int = 1) -> date:
        """
        查找下N个工作日

        Args:
            date_input: 起始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            delta_days: 要找的第几个工作日（正数向前，负数向后）

        Returns:
            date: 目标工作日
        """
        current = self._parse_date(date_input)
        remaining = abs(delta_days)
        direction = 1 if delta_days > 0 else -1

        # 如果当前日期就是工作日且delta_days=0，直接返回
        if delta_days == 0 and self.is_workday(current):
            return current.date() if isinstance(current, datetime) else current

        while remaining > 0:
            current += timedelta(days=direction)
            if self.is_workday(current):
                remaining -= 1

        return current.date() if isinstance(current, datetime) else current

    def count_workdays(self, start_date: Union[datetime, date, str, int],
                       end_date: Union[datetime, date, str, int],
                       include_weekends: bool = True) -> int:
        """
        计算日期范围内的工作日数量

        Args:
            start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            include_weekends: 是否包含周末的调休工作日，默认True

        Returns:
            int: 日期范围内的工作日数量
        """
        return len(self.get_workdays_in_range(start_date, end_date, include_weekends))

    def count_holidays(self, start_date: Union[datetime, date, str, int],
                       end_date: Union[datetime, date, str, int],
                       include_weekends: bool = True) -> int:
        """
        计算日期范围内的节假日数量
        Args:
            start_date: 开始日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            end_date: 结束日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串
            include_weekends: 是否包含普通周末，默认True

        Returns:
            int: 日期范围内的节假日数量
        """
        return len(self.get_holidays_in_range(start_date, end_date, include_weekends))

    def get_day_of_week(self, date_input: Union[datetime, date, str, int]) -> int:
        """
        获取日期是星期几

        Args:
            date_input: 日期对象，例如 2024-01-01

        Returns:
            int: 0、1、2、3、4、5、6，从0开始
        """
        return self.convert_str_to_date(self._normalize_date(date_input)).weekday()

    def _parse_date(self, date_input: Union[datetime, date, str, int]) -> datetime:
        """
        将日期输入解析为 datetime 对象

        Args:
            date_input: 日期

        Returns:
            datetime: 日期对象
        """
        if isinstance(date_input, str) or isinstance(date_input, int):
            return datetime.strptime(self._normalize_date(date_input), '%Y-%m-%d')
        elif isinstance(date_input, date) and not isinstance(date_input, datetime):
            return datetime.combine(date_input, datetime.min.time())
        elif isinstance(date_input, datetime):
            return date_input
        else:
            raise TypeError(f"Unsupported date type: {type(date_input)}")

    @staticmethod
    def _normalize_date(date_input: Union[datetime, date, str, int]) -> str:
        """
        将日期标准化为 YYYY-MM-DD 格式字符串

        Args:
            date_input: 日期，支持 datetime、date 或 'YYYY-MM-DD' 格式字符串

        Returns:
            str: 返回 YYYY-MM-DD 格式字符串
        """
        if isinstance(date_input, str):
            # 如果日期是字符串，且长度为10,
            if '-' in date_input and len(date_input) == 10:
                date_str_list = date_input.split('-')
                for dt_str in date_str_list:
                    if not bool(re.match(r'^\d+$', dt_str)):
                        raise ValueError(f"Invalid date format. Please use 'YYYY-MM-DD', 'YYYYMMDD', "
                                         f"or YYYYMMDD format: {date_input}")

                # 如果月是一位数，前面补0
                if 1 == len(date_str_list[1]):
                    month_str = "0" + date_str_list[1]
                else:
                    month_str = date_str_list[1]

                # 如果日是一位数，前面补0
                if 1 == len(date_str_list[2]):
                    day_str = "0" + date_str_list[2]
                else:
                    day_str = date_str_list[2]

                date_input = date_str_list[0] + "-" + month_str + "-" + day_str

            if '-' not in date_input and len(date_input) == 8:
                if not bool(re.match(r'^\d+$', date_input)):
                    raise ValueError(f"Invalid date format. Please use 'YYYY-MM-DD', 'YYYYMMDD', "
                                     f"or YYYYMMDD format: {date_input}")
                date_input = date_input[:4] + "-" + date_input[4:6] + "-" + date_input[6:]

            try:
                datetime.strptime(date_input, '%Y-%m-%d')
                return date_input
            except ValueError:
                raise ValueError(f"Invalid date format. Please use 'YYYY-MM-DD', 'YYYYMMDD', "
                                 f"or YYYYMMDD format: {date_input}")

        if isinstance(date_input, int):
            if len(str(date_input)) == 8:
                date_input = str(date_input)
                date_input = date_input[:4] + "-" + date_input[4:6] + "-" + date_input[6:]

            try:
                datetime.strptime(date_input, '%Y-%m-%d')
                return date_input
            except ValueError:
                raise ValueError(f"Invalid date format. Please use 'YYYY-MM-DD', 'YYYYMMDD', "
                                 f"or YYYYMMDD format: {date_input}")

        elif isinstance(date_input, (datetime, date)):
            return date_input.strftime('%Y-%m-%d')
        else:
            raise TypeError(f"不支持的日期类型：{type(date_input)}")

    @staticmethod
    def convert_str_to_datetime(y_m_d_str: str) -> datetime:
        """
        字符串年月日转换为日期对象返回

        Args:
            y_m_d_str: 2024-05-23

        Returns:
            datetime: 日期对象
        """
        return datetime.strptime(y_m_d_str, "%Y-%m-%d")

    @staticmethod
    def convert_str_to_date(y_m_d_str: str) -> date:
        """
        字符串年月日转换为日期对象返回

        Args:
            y_m_d_str: 2024-05-23

        Returns:
            date: 日期对象
        """
        return datetime.strptime(y_m_d_str, "%Y-%m-%d").date()

    @staticmethod
    def convert_date_obj_to_str(date_obj: datetime) -> str:
        """
        日期对象转换为字符串格式的日期返回

        Args:
            date_obj: 2024-05-23

        Returns:
            str: 2024-05-23
        """
        return date_obj.strftime("%Y-%m-%d")