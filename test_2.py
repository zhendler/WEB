import pandas as pd
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, 'uk_UA')




def generate_lessons(weekdays_A:list,weekdays_B:list=None,subject_name: str = "lesson"):
    if weekdays_B is None:
        weekdays_B = weekdays_A

    start_date = datetime(2024, 9, 2)  # First lesson on September 2nd
    holidays = [
        (datetime(2024, 10, 28), datetime(2024, 11, 3)),
        (datetime(2024, 12, 30), datetime(2025, 1, 12)),
        (datetime(2025, 3, 24), datetime(2025, 3, 30))
                ]

    # Lesson days: Monday, Wednesday, Friday
    # Monday = 0, Wednesday = 2, Friday = 4

    # Generate dates for lessons, skipping holidays
    lesson_dates = []
    current_date = start_date
    lesson_count = 1

    while current_date <= datetime(2025, 7, 1):
        if current_date.isocalendar()[1] % 2 == 0:
            weekdays = weekdays_A
        else:
            weekdays = weekdays_B
    if current_date.weekday():

