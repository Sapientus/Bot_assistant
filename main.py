from collections import UserDict
from functools import wraps

#This is a decorator to cope with exceptions
def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Phone number should be numeric and have at least 10 characters. Try again"
        except KeyError:
            return "This number doesn`t exist. Please, add it as a new number or try again."
        except TypeError:
            return "Please, type the proper command from the list of commands."

    return wrapper

#This class is a parent one for others, it defines logics.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

#This class saves contacts` names.
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

#This ones saves phone number.
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.check_phone_number()

    def check_phone_number(self):
        if self.value.isnumeric() and len(self.value) == 10:
            return self.value
        raise ValueError


#This class adds names with their phones to be able to add these records in an AddressBook
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    @input_error
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    #@input_error
    def edit_phone(self, old_phone, new_phone):
        if old_phone not in [i.value for i in self.phones]:
            raise ValueError('This phone number doesn\'t exist')
            
        self.remove_phone(old_phone)
        self.add_phone(new_phone)
        #for i in self.phones:
            #if i.value != old_phone:
                #raise ValueError('This phone number doesn\'t exist')
        #self.remove_phone(old_phone)
        #self.add_phone(new_phone)

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

#This class serves as a Dict to save our records and use methods for them
class AddressBook(UserDict):

    def add_record(self, Record):
        self.data[Record.name.value] = Record

    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
        return 'This contact doesn\'t exist.'

    def find(self, name):
        if name in self.data.keys():
            return self.data[name]
        return None