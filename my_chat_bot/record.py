from field import Name, Phone, Birthday

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, b_date):
        self.birthday = Birthday(b_date)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        old = Phone(old_phone)
        new = Phone(new_phone)

        for p in self.phones:
            if p.value == old.value:
                self.phones.remove(p)
                self.phones.append(new)
                return
        raise ValueError("Phone number not found")

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones}{birthday}"
