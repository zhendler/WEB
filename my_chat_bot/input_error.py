def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:  # недійсне значення
            return 'Give me name and phone, please.'
        except IndexError as e:  # неправильна кількість аргументів
            return f"Invalid number of arguments. Usage: {func.__name__} {e.args[0]}."
        except KeyError as e:  # ім'я не знайдено
            return f"Contact '{e.args[0]}' not found."
    return inner

def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, args
