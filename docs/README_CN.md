# 中国节假日查询库

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

<p align="center">
  简体中文 |
  <a href="../README.md">English</a>
</p>

## 概述

chinese-days - 专门用于查询中国节假日、调休工作日、补休日的Python库

### 项目结构

```reStructuredText
chinese-days/
├── chinesedays/
│   ├── __init__.py
│   ├── __version__.py		# 项目版本号
│   ├── calendar.py			# 日历工具
│   ├── date_utils.py		# 中国节假日、工作日查询工具便捷函数
│   ├── days_base.py		# 中国节假日、工作日查询类
│   ├── holiday.py			# 节假日对象类
│   └── holiday_type.py		# 节假日对象类
├── data/
│   └── chinese-days.json	# 中国节假日、工作日数据
├── docs/
│   └── README_CN.md		# 中文说明文档
├── examples/
│   ├── __init__.py
│   └── usage_examples.py	# 功能演示
├── tests/
│   ├── __init__.py
│   └── test_days.py		# 中国节假日、工作日库的完整测试用例
├── .gitignore
├── .python-version
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## 功能特性

- **多种日期类型支持**: `str`, `int`, `datetime`, `date`
- **节假日类型枚举**: 区分法定节假日、调休工作日、补休日
- **节假日名称查询**: 获取具体节假日名称（如"春节"、"国庆节"）
- **周末判断**: 独立的周末判断功能
- **include_weekends参数**: 灵活控制是否包含周末

## 安装

```bash
pip install chinese-days
```

或直接下载使用：

```bash
git clone https://github.com/Homalos/chinese-days.git
cd chinese-days
```

## 快速开始

### API示例

```python
from chinesedays.date_utils import (
    is_workday, is_holiday, is_weekend,
    get_workdays_in_range, get_holidays_in_range,
    find_next_workday, count_workdays, get_holiday_name,
    get_holidays, get_holiday_type
)

# 基本查询
print(is_holiday("2025-10-01"))    # True (国庆节)
print(is_workday("2025-10-01"))    # False (国庆节)
print(is_weekend("2025-09-06"))    # True (周六)
print(get_day_of_week("2025-09-30"))	# 1 (范围0-6，0是星期一以此类推)

# 获取节假日信息
print(get_holiday_name("2025-10-01"))  # "国庆节"

# 获取节假日类型
print(get_holiday_type("2025-10-01"))  # HolidayType.LEGAL
print(get_holiday_type("2025-10-11"))  # HolidayType.WORK （调休工作日）

# 查找下一个工作日
next_workday = find_next_workday("2025-10-01", 3)
print(next_workday)  # 2024-10-11

# 范围查询
workdays = get_workdays_in_range("2025-10-01", "2025-10-08")
holidays = get_holidays_in_range("2025-10-01", "2025-10-08")

print(f"工作日: {workdays}")  # []
print(f"节假日: {holidays}")  # [datetime.date(2025, 10, 1), ...]

# include_weekends参数控制
# 2025年春节假期不包含普通周末的节假日
holidays_workdays_only = get_holidays_in_range(
    "2025-01-28", "2025-02-04", include_weekends=False
)
print(f"2025年不包含周末的春节假期: {holidays_workdays_only}")
# [datetime.date(2025, 1, 28), ..., datetime.date(2025, 2, 3), datetime.date(2025, 2, 4)]

# 不包含周末调休的工作日
workdays_weekdays_only = get_workdays_in_range(
    "2025-10-06", "2025-10-12", include_weekends=False
)
print(f"不包含周末调休的工作日: {workdays_weekdays_only}")
# [datetime.date(2025, 10, 9), datetime.date(2025, 10, 10)]

# 统计功能
workday_count = count_workdays("2025-10-01", "2025-10-31")
print(f"2025年10月工作日数量: {workday_count}")  # 18

# 检查特定节假日
spring_festival = "2025-01-29"  # 春节
print(f"{spring_festival} 是否为节假日: {is_holiday(spring_festival)}")  # True
print(f"{spring_festival} 节假日名称: {get_holiday_name(spring_festival)}")  # 春节

# 获取2025年的所有节假日
holidays_2025 = get_holidays(2025)
print(f"2025年节假日数量: {len(holidays_2025)}")  # 28
for holiday in holidays_2025[:5]:  # 显示前5个
    print(f"{holiday.date} {holiday.name} ({holiday.english_name})")
    # 2025-01-01 元旦 (New Year's Day)
    # 2025-01-28 春节 (Spring Festival)
    # 2025-01-29 春节 (Spring Festival)
    # 2025-01-30 春节 (Spring Festival)
    # 2025-01-31 春节 (Spring Festival)

# 获取多个年份的节假日
holidays_multi = get_holidays([2024, 2025])
print(f"\n2024-2025年节假日数量: {len(holidays_multi)}")  # 56

# 获取春节相关的节假日
spring_festivals = [h for h in holidays_2025 if "春节" in h.name]
print("\n2025年春节假期:")
for holiday in spring_festivals:
    print(f"{holiday.date} {holiday.name}")
    # 2025-01-28 春节
    # 2025-01-29 春节
    # 2025-01-30 春节
    # 2025-01-31 春节
    # 2025-02-01 春节
    # 2025-02-02 春节
    # 2025-02-03 春节
    # 2025-02-04 春节

# 获取所有年份的元旦节假日
all_holidays = get_holidays()
new_year_days = [h for h in all_holidays if "元旦" in h.name]
print(f"\n所有年份元旦节假日数量: {len(new_year_days)}")  # 51
```

## 数据覆盖范围

- **时间范围**: 2004年 - 2026年
- **节假日类型**: 元旦、春节、清明节、劳动节、端午节、中秋节、国庆节
- **调休数据**: 包含完整的调休工作日和补休日信息
- **数据来源**: 基于 [vsme/chinese-days](https://github.com/vsme/chinese-days) 项目

## API参考

### 基础查询函数

| 函数                                 | 描述                       | 返回类型                |
| ------------------------------------ | -------------------------- | ----------------------- |
| `is_workday(date)`                   | 判断是否为工作日           | `bool`                  |
| `is_holiday(date)`                   | 判断是否为节假日           | `bool`                  |
| `is_weekend(date)`                   | 判断是否为周末             | `bool`                  |
| `get_holidays(years)`                | 获取节假日                 | `list[Holiday]`         |
| `get_holiday_type(date)`             | 获取节假日类型             | `Optional[HolidayType]` |
| `get_holiday_name(date)`             | 获取节假日名称             | `Optional[str]`         |
| `convert_str_to_datetime(y_m_d_str)` | 字符串年月日转换为日期对象 | `datetime`              |
| `convert_date_obj_to_str(datetime)`  | 日期对象转换为字符串       | `str`                   |
| `get_day_of_week(date)`              | 获取日期是星期几           | `int`                   |

### 范围查询函数

| 函数                                                         | 描述                       | 参数                                 | 返回类型     |
| ------------------------------------------------------------ | -------------------------- | ------------------------------------ | ------------ |
| `get_workdays_in_range(start, end, include_weekends=True)`   | 获取范围内工作日           | `include_weekends`: 是否包含周末调休 | `list[date]` |
| `get_holidays_in_range(start, end, include_weekends=True)`   | 获取范围内节假日           | `include_weekends`: 是否包含普通周末 | `list[date]` |
| `count_workdays(start, end, include_weekends=True)`          | 统计日期范围内工作日数量   | `include_weekends`: 是否包含普通周末 | `int`        |
| `count_holidays(start_date, end_date, include_weekends=True)` | 统计日期范围内的节假日数量 | `include_weekends`: 是否包含普通周末 | `int`        |

### 日期计算函数

| 函数                                    | 描述            | 返回类型 |
| --------------------------------------- | --------------- | -------- |
| `find_next_workday(date, delta_days=1)` | 查找第N个工作日 | `date`   |

## 运行测试

```bash
# 运行完整测试用例
python test_days.py

# 运行功能演示
python usage_examples.py
```

## 贡献

欢迎提交Issue和Pull Request

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 致谢

- [vsme/chinese-days](https://github.com/vsme/chinese-days) - 节假日数据来源

---

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**