from functools import wraps

user_input_dict = {}
bot_working = True


# It`s a decorator that copes with errors and returns strings as a reply to commands
def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Phone number should be numeric and have at least 10 characters. Try again"
        except KeyError:
            return "This number doesn`t exist. Please, add it as a new number or try again."
        except IndexError:
            return  "Please, try again"
        except TypeError:
            return "Please, type the proper command from the list of commands."

    return wrapper


# Here we are being polite and greet our user :)
@input_error
def greeting(username):
    return f"How can I help you {username}?"


# This checks if the phone number is correctly typed
@input_error
def check_phone_number(phone_number):
    if phone_number.isnumeric() and len(phone_number) >= 10:
        return phone_number


# This one adds new contacts
@input_error
def adding(user_input):
    if check_phone_number(user_input.split(" ")[-1]):
        user_input_dict[user_input.split(" ")[0]] = user_input.split(" ")[-1]
        return "Great, number was successfully added."
    raise ValueError


# Here we may change our contacts` phone number
@input_error
def changing(user_input):
    if check_phone_number(user_input.split(" ")[-1]):
        user_input_dict[user_input.split(" ")[0]] = user_input.split(" ")[-1]
        return "Number was successfully changed."
    raise ValueError


# Here we`re looking for needed phone number
@input_error
def search_phone(user_input):
    return user_input_dict.get(user_input)


# This shows us all saved numbers
@input_error
def show_all(username):
    table = "|{:*^41}|\n".format(f"All {username}'s phone numbers")
    for name, phone in user_input_dict.items():
        table += "|{:<20}|{:>20}|\n".format(name, phone)
    return table


# Here we stop our working when user enters stop-word
@input_error
def closing(username):
    global bot_working
    bot_working = False
    return f"Good bye {username}!"


# Here we create a dictionary for dividing commands and making code universal
commands_dict = {
    "hello": greeting,
    "add": adding,
    "change": changing,
    "phone": search_phone,
    "show all": show_all,
    "good bye": closing,
    "exit": closing,
    "close": closing,
}


# This function gets a certain command from dictionary when needed
def get_handler(command):
    return commands_dict[command]


def command_parser(user_input):
    for key in commands_dict:
        if key in user_input:
            return key


def main():
    global bot_working
    username = input("Enter username: ")
    while bot_working:
        user_input = input("Input the command: ")
        needed_command = command_parser(user_input)
        needed_argument = user_input.removeprefix(needed_command)
        if not needed_argument:
            print(get_handler(needed_command)(username))
        else:
            print(get_handler(needed_command)(needed_argument.lstrip()))


if __name__ == "__main__":
    main()
