import re
import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must be 10 digits")

        valid_number = re.sub(r'[^\d+ ]', '', value)
        valid_number = valid_number.replace(' ', '') 
        while len(valid_number) > 10:
            valid_number = valid_number[1:]

        value = ('+38' + valid_number)
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            day, month, year = map(int, value.split('.'))
            self.value = datetime.date(year, month, day)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')
