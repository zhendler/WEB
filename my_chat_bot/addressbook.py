from collections import UserDict
import datetime
import calendar
from record import Record


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value  # Отримуємо дату народження
                birthday_this_year = birthday.replace(year=today.year)

                # Перевіряємо, чи день народження в цьому році вже був
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)

                # Перевіряємо, чи день народження в наступні 7 днів
                if today <= birthday_this_year <= today + datetime.timedelta(days=7):
                    # Перевіряємо, чи день народження не випадає на вихідний
                    weekday = calendar.weekday(birthday_this_year.year, birthday_this_year.month, birthday_this_year.day)
                    if weekday >= 5:  # 5 - п'ятниця, 6 - субота
                        while calendar.weekday(birthday_this_year.year, birthday_this_year.month, birthday_this_year.day) >= 5:
                            birthday_this_year += datetime.timedelta(days=1)

                    upcoming_birthdays.append({"name": record.name.value, "birthday": birthday_this_year})

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
