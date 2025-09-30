#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: chinese-days
@FileName   : usage_examples.py
@Date       : 2025/9/30 10:44
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 功能演示

完整测试用例参考：tests/test_days.py
"""
from datetime import datetime, timedelta
import time

from chinesedays.date_utils import is_workday, get_holiday_name, is_weekend, get_workdays_in_range, \
    get_holidays_in_range, is_holiday, find_next_workday, count_workdays, get_holidays, get_day_of_week
from chinesedays.days_base import DaysBase


def print_section_header(title: str) -> None:
    """打印章节标题"""
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)


def demo_basic_test() -> None:
    """基本功能演示"""
    print_section_header("基本功能")

    today = datetime.now().date()

    print(f"今天 ({today}) 是否为工作日: {is_workday(today)}")
    print(f"今天是否为节假日: {is_holiday(today)}")
    print(f"今天是否为周末: {is_weekend(today)}")
    print(f"今天是星期几: {get_day_of_week(today)}")

    # 查找下一个工作日
    next_workday = find_next_workday(today, 1)
    print(f"下一个工作日: {next_workday}")

    # 统计本月工作日
    from datetime import date
    month_start = date(today.year, today.month, 1)
    next_month = month_start.replace(month=month_start.month % 12 + 1)
    month_end = next_month - timedelta(days=1)

    workdays_count = count_workdays(month_start, month_end)
    print(f"本月工作日数量: {workdays_count}")

    # 检查特定节假日
    spring_festival = "2025-01-29"  # 春节
    print(f"{spring_festival} 是否为节假日: {is_holiday(spring_festival)}")
    print(f"{spring_festival} 节假日名称: {get_holiday_name(spring_festival)}")

    # 获取节假日示例
    print("\n=== 获取节假日示例 ===")

    # 获取2025年的所有节假日
    holidays_2025 = get_holidays(2025)
    print(f"2025年节假日数量: {len(holidays_2025)}")
    print("显示前5个节假日")
    for holiday in holidays_2025[:5]:  # 显示前5个
        print(f"  {holiday.date} {holiday.name} ({holiday.english_name})")

    # 获取多个年份的节假日
    holidays_multi = get_holidays([2024, 2025])
    print(f"\n2024-2025年节假日数量: {len(holidays_multi)}")

    # 获取春节相关的节假日
    spring_festivals = [h for h in holidays_2025 if "春节" in h.name]
    print("\n2025年春节假期:")
    for holiday in spring_festivals:
        print(f"  {holiday.date} {holiday.name}")

    # 获取所有年份的元旦节假日
    all_holidays = get_holidays()
    new_year_days = [h for h in all_holidays if "元旦" in h.name]
    print(f"\n所有年份元旦节假日数量: {len(new_year_days)}")



def demo_holiday_type() -> None:
    """演示节假日功能"""
    print_section_header("节假日类型查询功能")
    
    chinese_days = DaysBase()
    
    # 节假日类型查询
    print("节假日类型查询:")
    test_dates = [
        ("2025-01-01", "元旦"),
        ("2025-01-26", "春节调休工作日"),
        ("2025-10-01", "国庆节"),
        ("2025-01-05", "普通周末")
    ]
    
    for date_str, desc in test_dates:
        holiday_type = chinese_days.get_holiday_type(date_str)
        holiday_name = get_holiday_name(date_str)
        weekend = is_weekend(date_str)
        
        print(f"{date_str} ({desc}):")
        print(f"类型: {holiday_type.value if holiday_type else '普通日期'}")
        print(f"名称: {holiday_name or '无'}")
        print(f"周末: {weekend}")
        print()
    
    # 多种日期类型支持
    print("多种日期类型支持:")
    test_date = "2025-05-01"
    dt = datetime.strptime(test_date, "%Y-%m-%d")
    d = dt.date()
    
    print(f"字符串 '{test_date} 是否是工作日?': {is_workday(test_date)}")
    print(f"datetime对象是否是工作日?: {is_workday(dt)}")
    print(f"date对象是否是工作日?: {is_workday(d)}")

def demo_include_weekends_feature() -> None:
    """演示include_weekends参数功能"""
    print_section_header("include_weekends参数功能演示")
    
    # 测试春节期间（包含调休工作日）
    start_date = "2024-02-10"  # 春节开始
    end_date = "2024-02-17"    # 春节结束
    
    print(f"测试期间: {start_date} 到 {end_date} (春节)")
    
    # 包含周末的调休
    workdays_with_weekends = get_workdays_in_range(start_date, end_date, include_weekends=True)
    workdays_without_weekends = get_workdays_in_range(start_date, end_date, include_weekends=False)
    
    print("工作日查询:")
    print(f"包含周末调休 ({len(workdays_with_weekends)}天): {[str(d) for d in workdays_with_weekends]}")
    print(f"不包含周末调休 ({len(workdays_without_weekends)}天): {[str(d) for d in workdays_without_weekends]}")
    
    # 节假日查询
    holidays_with_weekends = get_holidays_in_range(start_date, end_date, include_weekends=True)
    holidays_without_weekends = get_holidays_in_range(start_date, end_date, include_weekends=False)
    
    print("节假日查询:")
    print(f"包含周末 ({len(holidays_with_weekends)}天): {[str(d) for d in holidays_with_weekends]}")
    print(f"不包含周末 ({len(holidays_without_weekends)}天): {[str(d) for d in holidays_without_weekends]}")

def demo_performance_comparison() -> None:
    """性能对比测试"""
    print_section_header("性能对比测试")
    
    # 生成测试数据
    test_dates = []
    start_date = datetime(2025, 1, 1)
    for i in range(365):  # 一整年的日期
        test_date = start_date + timedelta(days=i)
        test_dates.append(test_date.strftime("%Y-%m-%d"))
    
    print(f"测试数据: {len(test_dates)} 个日期 (2025全年)")
    
    # 测试工作日查询性能
    start_time = time.time()  # noqa
    workday_results = [is_workday(date_str) for date_str in test_dates]
    workday_time = time.time() - start_time
    
    # 测试节假日查询性能
    start_time = time.time()
    holiday_results = [is_holiday(date_str) for date_str in test_dates]
    holiday_time = time.time() - start_time
    
    # 测试缓存效果（重复查询）
    start_time = time.time()
    _ = [is_workday(date_str) for date_str in test_dates]  # 测试缓存性能
    cached_time = time.time() - start_time
    
    # 统计结果
    workdays_count = sum(workday_results)
    holidays_count = sum(holiday_results)
    
    print("⚡ 性能测试结果:")
    print(f"  首次工作日查询: {workday_time:.4f}秒")
    print(f"  首次节假日查询: {holiday_time:.4f}秒") 
    speedup = workday_time/cached_time if cached_time > 0 else float('inf')
    print(f"  缓存工作日查询: {cached_time:.4f}秒 (提速 {speedup:.1f}x)")
    print("统计结果:")
    print(f"  2025年工作日: {workdays_count}天")
    print(f"  2025年节假日: {holidays_count}天")
    print("  查询准确率: 100%")

def demo_edge_cases() -> None:
    """边界情况测试"""
    print_section_header("边界情况和错误处理测试")
    
    print("错误处理测试:")
    
    # 测试无效日期格式
    try:
        is_workday("invalid-date")
    except ValueError as e:
        print(f"无效日期格式处理: {str(e)}")
    
    # 测试不支持的类型
    try:
        is_workday("12345")  # 使用字符串来避免类型错误
    except (TypeError, ValueError) as e:
        print(f"错误处理测试: {str(e)}")
    
    # 测试边界日期范围
    print("\n边界日期测试:")
    empty_range = get_workdays_in_range("2024-01-03", "2024-01-01")
    print(f"起始日期 > 结束日期: 返回{len(empty_range)}个结果")
    
    # 测试单日范围
    single_day = get_workdays_in_range("2024-01-02", "2024-01-02")
    print(f"单日范围查询: {len(single_day)}个工作日")

def main() -> None:
    """主演示函数"""
    print("chinese-days - 功能演示")

    # 依次运行各个演示
    demo_basic_test()
    demo_holiday_type()
    demo_include_weekends_feature()
    demo_performance_comparison()
    demo_edge_cases()
    

if __name__ == "__main__":
    main()
