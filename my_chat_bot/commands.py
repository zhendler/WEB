from input_error import input_error
from addressbook import AddressBook
from record import Record

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."
    return str(record)

@input_error
def show_all_contacts(book):
    if not book:
        return "The phone book is empty."
    return str(book)

@input_error
def add_birthday(args, book):
    name, b_date = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(b_date)
    return f"Birth date for {name} added/updated."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."
    if record.birthday:
        return f"Birthday of {name} is {record.birthday.value}"
    return f"No birthday set for {name}."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{item['name']} - {item['birthday']}" for item in upcoming])
