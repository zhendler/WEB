from console_view import ConsoleView
from addressbook import AddressBook
from commands import add_contact, show_phone, show_all_contacts, add_birthday, show_birthday, birthdays
from input_error import parse_input
from load_saver import save_data , load_data

def main():
    book = load_data()
    view = ConsoleView()
    view.display_help()
    while True:
        
        user_input = view.get_input("Enter a command: ")
        command, args = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) != 2:
                view.display_massage("Invalid number of arguments. Usage: add [name] [phone number]")
                continue
            view.display_massage(add_contact(args, book))
            save_data(book)
        elif command == "show":
            if not args:
                view.display_massage("Please specify a contact name.")
                continue
            view.display_contact(show_phone(args, book))
        elif command == "all":
            view.display_contacts(show_all_contacts(book))
        elif command == "add-birthday":
            view.display_massage(add_birthday(args, book))
            save_data(book)
        elif command == "show-birthday":
            view.display_massage(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "help":
            view.display_help()
        elif command in ("close", "exit"):
            view.display_massage("Good bye!")
            save_data(book)
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
