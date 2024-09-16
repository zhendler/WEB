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

        if current_date.weekday() in weekdays:
            # Check if the current date falls within any holiday period
            if not any(holiday[0] <= current_date <= holiday[1] for holiday in holidays):
                lesson_dates.append([lesson_count, current_date.strftime('%d.%m'), current_date.strftime('%A')])
                lesson_count += 1
        current_date += timedelta(days=1)

    # Create a DataFrame
    df_lessons = pd.DataFrame(lesson_dates, columns=['Lesson Number', 'Date', 'Day of the Week'])

    # Show the result
    #df_lessons.head(20)
    # Save the DataFrame to an Excel file
    file_name = f"{subject_name}.xlsx"
    df_lessons.to_excel(file_name, index=False)


if __name__ == '__main__':
    generate_lessons(weekdays_A=[0, 2, 4], weekdays_B=[0, 1, 2, 4], subject_name="Література")
    generate_lessons(weekdays_A=[0, 1, 2, 3, 4],  subject_name="Математика")
    generate_lessons(weekdays_A=[0, 2, 4],  subject_name="Мистецтво")





# Monday = 0, Wednesday = 2, Friday = 4