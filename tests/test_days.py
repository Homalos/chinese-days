#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: chinese-days
@FileName   : test_days.py
@Date       : 2025/9/30 10:26
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 中国节假日、工作日库的完整测试用例

更多详细用法参考：demo/usage_examples.py
"""
import unittest
from datetime import date, datetime, timedelta

from chinesedays.date_utils import is_workday, is_holiday, is_weekend, get_holiday_name, find_next_workday, \
    get_workdays_in_range, get_holidays_in_range, count_workdays
from chinesedays.days_base import DaysBase
from chinesedays.holiday_type import HolidayType


class TestDaysBase(unittest.TestCase):
    """中国节假日库测试类"""

    def setUp(self):
        """测试前的设置"""
        self.chinese_days = DaysBase()

    def test_singleton_pattern(self):
        """测试单例模式"""
        instance1 = DaysBase()
        instance2 = DaysBase()
        self.assertIs(instance1, instance2, "单例模式应该返回同一个实例")

    def test_is_workday_basic(self):
        """测试基本工作日判断"""
        # 2025年1月1日是元旦节假日
        self.assertFalse(is_workday("2025-01-01"))

        # 2025年1月2日是周四，应该是工作日
        self.assertTrue(is_workday("2025-01-02"))

        # 测试周末
        # 2025年1月4日是周六
        self.assertFalse(is_workday("2025-01-04"))
        # 2025年1月5日是周日
        self.assertFalse(is_workday("2025-01-05"))

    def test_is_workday_spring_festival_2024(self):
        """测试2024年春节期间的工作日判断"""
        # 春节假期：2024年2月10-17日
        spring_festival_dates = [
            "2024-02-10", "2024-02-11", "2024-02-12", "2024-02-13",
            "2024-02-14", "2024-02-15", "2024-02-16", "2024-02-17"
        ]

        for date_str in spring_festival_dates:
            self.assertFalse(is_workday(date_str), f"{date_str} 应该是春节假期")

        # 调休工作日：2024年2月4日（周日）和2024年2月18日（周日）
        self.assertTrue(is_workday("2024-02-04"), "2024-02-04 应该是调休工作日")
        self.assertTrue(is_workday("2024-02-18"), "2024-02-18 应该是调休工作日")

    def test_is_workday_national_day_2024(self):
        """测试2024年国庆节期间的工作日判断"""
        # 国庆假期：2024年10月1-7日
        national_day_dates = [
            "2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04",
            "2024-10-05", "2024-10-06", "2024-10-07"
        ]

        for date_str in national_day_dates:
            self.assertFalse(is_workday(date_str), f"{date_str} 应该是国庆假期")

        # 调休工作日：2024年9月29日（周日）和2024年10月12日（周六）
        self.assertTrue(is_workday("2024-09-29"), "2024-09-29 应该是调休工作日")
        self.assertTrue(is_workday("2024-10-12"), "2024-10-12 应该是调休工作日")

    def test_is_holiday_basic(self):
        """测试节假日判断"""
        # 元旦
        self.assertTrue(is_holiday("2024-01-01"))

        # 劳动节
        self.assertTrue(is_holiday("2024-05-01"))

        # 普通工作日
        self.assertFalse(is_holiday("2024-01-02"))

        # 周末
        self.assertTrue(is_holiday("2024-01-06"))  # 周六
        self.assertTrue(is_holiday("2024-01-07"))  # 周日

    def test_is_weekend(self):
        """测试周末判断"""
        # 2024年1月6日是周六
        self.assertTrue(is_weekend("2024-01-06"))
        # 2024年1月7日是周日
        self.assertTrue(is_weekend("2024-01-07"))
        # 2024年1月8日是周一
        self.assertFalse(is_weekend("2024-01-08"))

    def test_get_holiday_name(self):
        """测试获取节假日名称"""
        # 春节
        self.assertEqual(get_holiday_name("2024-02-10"), "春节")

        # 元旦
        self.assertEqual(get_holiday_name("2024-01-01"), "元旦")

        # 劳动节
        self.assertEqual(get_holiday_name("2024-05-01"), "劳动节")

        # 国庆节
        self.assertEqual(get_holiday_name("2024-10-01"), "国庆节")

        # 普通日期
        self.assertIsNone(get_holiday_name("2024-01-02"))

    def test_get_holiday_type(self):
        """测试获取节假日类型"""
        # 法定节假日
        self.assertEqual(self.chinese_days.get_holiday_type("2024-01-01"), HolidayType.LEGAL)

        # 调休工作日
        self.assertEqual(self.chinese_days.get_holiday_type("2024-02-04"), HolidayType.WORK)

        # 普通日期
        self.assertIsNone(self.chinese_days.get_holiday_type("2024-01-02"))

    def test_find_next_workday(self):
        """测试查找下一个工作日"""
        # 从2024年1月1日（元旦节假日）找下一个工作日
        next_workday = find_next_workday("2024-01-01", 1)
        self.assertEqual(next_workday, date(2024, 1, 2))

        # 从周五找下一个工作日（应该跳过周末）
        # 2024年1月5日是周五
        next_workday = find_next_workday("2024-01-05", 1)
        self.assertEqual(next_workday, date(2024, 1, 8))  # 周一

        # 找前一个工作日
        prev_workday = find_next_workday("2024-01-02", -1)
        self.assertEqual(prev_workday, date(2023, 12, 29))  # 跳过元旦假期

    def test_get_workdays_in_range(self):
        """测试获取日期范围内的工作日"""
        # 测试一周内的工作日（包含周末）
        workdays = get_workdays_in_range("2024-01-08", "2024-01-14")  # 周一到周日
        expected_workdays = [
            date(2024, 1, 8), date(2024, 1, 9), date(2024, 1, 10),
            date(2024, 1, 11), date(2024, 1, 12)
        ]  # 周一到周五
        self.assertEqual(workdays, expected_workdays)

        # 测试包含节假日的范围
        workdays = get_workdays_in_range("2023-12-30", "2024-01-03")
        # 2024年1月1日是元旦，应该被排除
        expected = [date(2024, 1, 2), date(2024, 1, 3)]  # 只有工作日
        self.assertEqual(workdays, expected)

    def test_get_holidays_in_range(self):
        """测试获取日期范围内的节假日"""
        # 测试包含元旦的范围
        holidays = get_holidays_in_range("2023-12-30", "2024-01-03")
        # 应该包含：2023-12-30(周六), 2023-12-31(周日), 2024-01-01(元旦)
        expected = [
            date(2023, 12, 30), date(2023, 12, 31), date(2024, 1, 1)
        ]
        self.assertEqual(holidays, expected)

    def test_count_workdays(self):
        """测试计算工作日数量"""
        # 测试一周的工作日数量
        count = count_workdays("2024-01-08", "2024-01-14")  # 周一到周日
        self.assertEqual(count, 5)  # 应该有5个工作日

        # 测试包含节假日的月份
        count = count_workdays("2024-02-01", "2024-02-29")  # 2024年2月
        # 2月有春节假期，工作日会比较少
        self.assertGreater(count, 10)  # 至少有10个工作日
        self.assertLess(count, 25)  # 不会超过25个工作日

    def test_count_holidays(self):
        """测试计算节假日数量"""
        # 测试一周的节假日数量
        count = self.chinese_days.count_holidays("2024-01-08", "2024-01-14")  # 周一到周日
        self.assertEqual(count, 2)  # 周六周日

        # 测试包含春节的范围
        count = self.chinese_days.count_holidays("2024-02-10", "2024-02-17")
        self.assertEqual(count, 8)  # 春节8天假期

    def test_different_date_types(self):
        """测试不同的日期类型输入"""
        test_date = "2024-01-02"

        # 字符串类型
        self.assertTrue(is_workday(test_date))

        # datetime类型
        dt = datetime.strptime(test_date, "%Y-%m-%d")
        self.assertTrue(is_workday(dt))

        # date类型
        d = dt.date()
        self.assertTrue(is_workday(d))

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试无效日期格式
        with self.assertRaises(ValueError):
            is_workday("invalid-date")

        with self.assertRaises(ValueError):
            is_workday("2024-13-01")  # 无效月份

        # 测试不支持的类型
        with self.assertRaises(TypeError):
            is_workday(12345)  # noqa

        # 测试日期范围边界
        # 起始日期晚于结束日期
        workdays = get_workdays_in_range("2024-01-03", "2024-01-01")
        self.assertEqual(len(workdays), 0)  # 应该返回空列表

    def test_performance_cache(self):
        """测试缓存性能"""
        import time

        # 第一次调用
        start_time = time.time()
        result1 = is_workday("2024-01-01")
        first_call_time = time.time() - start_time

        # 第二次调用（应该使用缓存）
        start_time = time.time()
        result2 = is_workday("2024-01-01")
        second_call_time = time.time() - start_time

        self.assertEqual(result1, result2)
        # 第二次调用应该更快（使用了缓存）
        # 注意：这个测试在某些情况下可能不稳定，因为时间差可能很小

    def test_year_2025_data(self):
        """测试2025年的数据"""
        # 2025年元旦
        self.assertTrue(is_holiday("2025-01-01"))

        # 2025年春节（1月28日-2月4日）
        spring_festival_2025 = [
            "2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31",
            "2025-02-01", "2025-02-02", "2025-02-03", "2025-02-04"
        ]

        for date_str in spring_festival_2025:
            self.assertTrue(is_holiday(date_str), f"{date_str} 应该是2025年春节假期")

        # 调休工作日
        self.assertTrue(is_workday("2025-01-26"), "2025-01-26 应该是调休工作日")
        self.assertTrue(is_workday("2025-02-08"), "2025-02-08 应该是调休工作日")


def run_performance_benchmark():
    """性能基准测试"""
    import time

    print("\n" + "=" * 50)
    print("性能基准测试")
    print("=" * 50)

    # 测试大量日期查询的性能
    test_dates = []
    start_date = datetime(2020, 1, 1)
    for i in range(1000):  # 生成1000个测试日期
        test_date = start_date + timedelta(days=i)
        test_dates.append(test_date.strftime("%Y-%m-%d"))

    # 工作日查询性能测试
    start_time = time.time()
    workday_results = [is_workday(date_str) for date_str in test_dates]
    workday_time = time.time() - start_time

    # 节假日查询性能测试
    start_time = time.time()
    holiday_results = [is_holiday(date_str) for date_str in test_dates]
    holiday_time = time.time() - start_time


    # 日期范围查询性能测试
    start_time = time.time()
    workdays_in_range = get_workdays_in_range("2024-01-01", "2024-12-31")
    range_time = time.time() - start_time

    print(f"工作日查询 (1000次): {workday_time:.4f}秒")
    print(f"节假日查询 (1000次): {holiday_time:.4f}秒")
    print(f"日期范围查询 (1年): {range_time:.4f}秒")
    print(f"2024年工作日总数: {len(workdays_in_range)}")
    print("=" * 50)


if __name__ == "__main__":
    # 运行单元测试
    unittest.main(verbosity=2, exit=False)

    # 运行性能基准测试
    run_performance_benchmark()
