# Chinese Holiday and Working Day Lookup Library

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

<p align="center">
  English |
  <a href="docs/README_CN.md">简体中文</a>
</p>

## Overview

chinese-days is a Python library for querying Chinese holidays and working days.

### Project Structure

```reStructuredText
chinese-days/
├── chinesedays/
│   ├── __init__.py
│   ├── __version__.py		# Project version number
│   ├── calendar.py			# Calendar utility
│   ├── date_utils.py		# Utility functions for querying Chinese holidays and working days
│   ├── days_base.py		# Class for querying Chinese holidays and working days
│   ├── holiday.py			# Holiday object class
│   └── holiday_type.py		# Holiday type enumeration
├── data/
│   └── chinese-days.json	# Chinese holiday and working day data
├── docs/
│   └── README_CN.md		# Chinese instruction manual
├── examples/
│   ├── __init__.py
│   └── usage_examples.py	# Usage examples
├── tests/
│   ├── __init__.py
│   └── test_days.py		# Complete test suite for the Chinese holiday and working day library
├── .gitignore
├── .python-version
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## Features

- **Multiple date type support**: `str`, `int`, `datetime`, `date`
- **Holiday type enumeration**: Distinguishes between legal holidays, adjusted working days, and compensatory days off
- **Holiday name lookup**: Retrieves the specific holiday name (e.g., "Spring Festival", "National Day")
- **Weekend detection**: Independent weekend detection functionality
- **include_weekends parameter**: Flexible control to include or exclude weekends

## Installation

```bash
pip install chinese-days
```

Or download and use directly:

```bash
git clone https://github.com/Homalos/chinese-days.git
cd chinese-days
```

## Quick Start

### API Examples

```python
from chinesedays.date_utils import (
is_workday, is_holiday, is_weekend,
get_workdays_in_range, get_holidays_in_range,
find_next_workday, count_workdays, get_holiday_name,
get_holidays, get_holiday_type
)

# Basic queries
print(is_holiday("2025-10-01"))    # True (National Day)
print(is_workday("2025-10-01"))    # False (National Day)
print(is_weekend("2025-09-06"))    # True (Saturday)
print(get_day_of_week("2025-09-30"))  # 1 (range 0-6, 0 is Monday, etc.)

# Get holiday information
print(get_holiday_name("2025-10-01"))  # "National Day"

# Get holiday type
print(get_holiday_type("2025-10-01"))  # HolidayType.LEGAL
print(get_holiday_type("2025-10-11"))  # HolidayType.WORK (makeup workday)

# Find the next workday
next_workday = find_next_workday("2025-10-01", 3)
print(next_workday)  # 2024-10-11

# Range query
workdays = get_workdays_in_range("2025-10-01", "2025-10-08")
holidays = get_holidays_in_range("2025-10-01", "2025-10-08")

print(f"Workdays:")
​``` print(f"Workdays: {workdays}")  # []
print(f"Holidays: {holidays}")  # [datetime.date(2025, 10, 1), ...]

# Controlling the 'include_weekends' parameter
# Spring Festival holidays in 2025, excluding regular weekends
holidays_workdays_only = get_holidays_in_range(
"2025-01-28", "2025-02-04", include_weekends=False
)
print(f"Spring Festival holidays in 2025 (excluding weekends): {holidays_workdays_only}")
# [datetime.date(2025, 1, 28), ..., datetime.date(2025, 2, 3), datetime.date(2025, 2, 4)]

# Workdays excluding weekend adjustments
workdays_weekdays_only = get_workdays_in_range(
"2025-10-06", "2025-10-12", include_weekends=False
)
print(f"Workdays excluding weekend adjustments: {workdays_weekdays_only}")
# [datetime.date(2025, 10, 9), datetime.date(2025, 10, 10)]

# Counting function
workday_count = count_workdays("2025-10-01", "2025-10-31")
print(f"Number of workdays in October 2025: {workday_count}")  # 18

# Checking a specific holiday
spring_festival = "2025-01-29"  # Spring Festival
print(f"{spring_festival} is a holiday: {is_holiday(spring_festival)}")  # True
print(f"Name of the holiday on {spring_festival}: {get_holiday_name(spring_festival)}")  # Spring Festival

# Get all holidays in 2025
holidays_2025 = get_holidays(2025)
print(f"Number of holidays in 2025: {len(holidays_2025)}")  # 28
for holiday in holidays_2025[:5]:  # Display the first 5 holidays
print(f"{holiday.date} {holiday.name} ({holiday.english_name})")
# 2025-01-01 New Year's Day (New Year's Day)
# 2025-01-28 Spring Festival (Spring Festival)
# 2025-01-29 Spring Festival (Spring Festival)
# 2025-01-30 Spring Festival (Spring Festival)
# 2025-01-31 Spring Festival (Spring Festival)

# Get holidays for multiple years
holidays_multi = get_holidays([2024, 2025])
print(f"\nNumber of holidays from 2024 to 2025: {len(holidays_multi)}")  # 56

# Get Spring Festival holidays
spring_festivals = [h for h in holidays_2025 if "Spring Festival" in h.name]
print("\nSpring Festival holidays in 2025:")
for holiday in spring_festivals:
print(f"{holiday.date} {holiday.name}")
# 2025-01-28 Spring Festival
# 2025-01-29 Spring Festival
# 2025-01-30 Spring Festival
# 2025-01-31 Spring Festival
# 2025-02-01 Spring Festival
# 2025-02-02 Spring Festival
# 2025-02-03 Spring Festival
# 2025-02-04 Spring Festival

# Get all New Year's Day holidays
all_holidays = get_holidays()
new_year_days = [h for h in all_holidays if "New Year's Day" in h.name]
print(f"\nNumber of New Year's Day holidays across all years: {len(new_year_days)}")  # 51
```

## Data Coverage

- **Time Period**: 2004 - 2025
- **Holiday Types**: New Year's Day, Spring Festival, Tomb-Sweeping Festival, Labor Day, Dragon Boat Festival, Mid-Autumn Festival, National Day
- **Adjusted Workdays and Compensatory Days**: Includes complete information on adjusted workdays and compensatory days
- **Data Source**: Based on the [vsme/chinese-days](https://github.com/vsme/chinese-days) project

## API Reference

### Basic Query Functions

| Function                             | Description                              | Return Type             |
| ------------------------------------ | ---------------------------------------- | ----------------------- |
| `is_workday(date)`                   | Check if a date is a workday             | `bool`                  |
| `is_holiday(date)`                   | Check if a date is a holiday             | `bool`                  |
| `is_weekend(date)`                   | Check if a date is a weekend             | `bool`                  |
| `get_holidays(years)`                | Get a list of holidays                   | `list[Holiday]`         |
| `get_holiday_type(date)`             | Get the type of a holiday                | `Optional[HolidayType]` |
| `get_holiday_name(date)`             | Get the name of a holiday                | `Optional[str]`         |
| `convert_str_to_datetime(y_m_d_str)` | Convert a date string to datetime object | `datetime`              |
| `convert_date_obj_to_str(datetime)`  | Convert a datetime object to string      | `str`                   |
| `get_day_of_week(date)`              | Get the day of the week                  | `int`                   |

### Range Query Functions

| Function                                                     | Description                             | Parameters                            | Return Type  |
| ------------------------------------------------------------ | --------------------------------------- | ------------------------------------- | ------------ |
| `get_workdays_in_range(start, end, include_weekends=True)`   | Get workdays within a date range        | `include_weekends`: Include weekends? | `list[date]` |
| `get_holidays_in_range(start, end, include_weekends=True)`   | Get holidays within a date range        | `include_weekends`: Include weekends? | `list[date]` |
| `count_workdays(start, end, include_weekends=True)`          | Count the number of workdays in a range | `include_weekends`: Include weekends? | `int`        |
| `count_holidays(start_date, end_date, include_weekends=True)` | Count the number of holidays in a range | `include_weekends`: Include weekends? | `int`        |

### Date Calculation Functions

| Function                                | Description              | Return Type |
| --------------------------------------- | ------------------------ | ----------- |
| `find_next_workday(date, delta_days=1)` | Find the Nth working day | `date`      |

## Running Tests

```bash
# Run the full test suite
python test_days.py

# Run usage examples
python usage_examples.py
```

## Contributing

We welcome issues and pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [vsme/chinese-days](https://github.com/vsme/chinese-days) - Holiday data source

---

**If this project has been helpful to you, please give it a ⭐ Star to show your support!**