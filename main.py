from collections import UserDict
from collections.abc import Iterator
from functools import wraps
from datetime import datetime, date     #To count days till the birthday

#This is a decorator to cope with exceptions
def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Wrong value. The phine nu,ber should consists of 10 digits and the birthday should be 'YYYY-mm-dd'!"
        except KeyError:
            return "This number doesn`t exist. Please, add it as a new number or try again."
        except TypeError:
            return "You inputed the wrong type. All the data shoul be string type."

    return wrapper

#This class is a parent one for others, it defines logics.
class Field:
    def __init__(self, value):
        self._value = value

    @property       #I wrote here just a property decorator `cause it will be common for other classes
    def value(self):
        return self._value
    

    def __str__(self):
        return str(self._value)
    
class Birthday(Field):

    def __init__(self, value: int):
        self._value = None
        if value:
            try:
                self._value = datetime.strptime(value, "%Y-%m-%d")
            except TypeError:
                print('Birthday should be a string type!')
        self.check_birthday(value)

    @input_error       
    def check_birthday(self, value):     #This returns a string if birthdays is wrong, and None if it is correct
        if datetime.strptime(value, "%Y-%m-%d"):
            return None

    @Field.value.setter            #A setter for our birthday
    def value(self, new_value):
        if not self.check_birthday(new_value):
            self._value = new_value
        

#This class saves contacts` names.
class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self._value = self._value.capitalize()

    @Field.value.setter          #This one lets us set the correct name
    def value(self, new_value):
        if new_value.isalpha():
            self._value = new_value.capitalize()

#This one saves phone number.
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.check_phone_number(value)    

    def check_phone_number(self, new_value):
        if new_value.isnumeric() and len(new_value) == 10:
            return new_value
        raise ValueError
    
    @Field.value.setter               #I add a setter here to let an user set the phone
    def value(self, new_value):
        if self.check_phone_number(new_value):
            self._value = new_value


#This class adds names with their phones to be able to add these records in an AddressBook
class Record:
    def __init__(self, value, birthday=None):
        self.name = Name(value)
        self.phones = []
        self.birthday = Birthday(birthday)

    @input_error
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

    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i
        return None
    
    def days_to_birthday(self):       #This method counts the amount of days till birthday
        today = date.today()
        if self.birthday:
            birthday_nowadays = self.birthday.value.date().replace(year=today.year)
            if today>birthday_nowadays:
                birthday_nowadays = birthday_nowadays.replace(year=today.year+1)
            days_till_birthday = (birthday_nowadays - today).days
            return f'Days till the {self.name}\'s birthday: {days_till_birthday}'

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

#This class serves as a Dict to save our records and use methods for them
class AddressBook(UserDict):

    def __init__(self):
        super().__init__()

    def add_record(self, Record):
        self.data[Record.name.value] = str(Record)

    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
        return 'This contact doesn\'t exist.'

    def find(self, name):
        if name in self.data.keys():
            return self.data[name]
        return None

    #Here we create an iter method for our generator
    def __iter__(self) -> Iterator:
        return self.iterator()
    
    def iterator(self, N):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i + N]
    
if __name__ == '__main__':
    
    #Here I create instances of Record class
    john = Record('john')
    kate = Record('kate', '1990-10-10')
    matt = Record('matt')
    bill = Record('bill')

    #Here I check if the birthda was counted correctly
    print(kate.days_to_birthday())

    #Here I check if the exceptions are handled correctly
    jack = Record('jack', 78989879)
    jack.add_phone('1376')
    jess = Record('jess12')

    #Here I add instances to the address book.
    john.add_phone('1234567890')
    matt.add_phone('1230987654')
    kate.add_phone('1234560987')
    bill.add_phone('1234567809')

    #Here I create an address book and add instances.
    address = AddressBook()
    address.add_record(john)
    address.add_record(matt)
    address.add_record(kate)
    address.add_record(bill)

    #Finally, this shitable generator
    for record in address.iterator(3):
        print(record)
