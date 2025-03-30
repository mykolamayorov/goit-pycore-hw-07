from collections import UserDict
from datetime import datetime, timedelta

# Base class for fields (like Name and Phone)
class Field:
    # Initialize with a value
    def __init__(self, value):
        self.value = value

    # Return the string representation of the field's value
    def __str__(self):
        return str(self.value)

# Name class inherits from Field, used for contact names
class Name(Field):
    # Initialize with a value and ensure it's not empty
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty") # Raise error if name is empty
        
        # Call the parent class constructor to set value
        super().__init__(value)

# Phone class inherits from Field, used for phone numbers
class Phone(Field):
    # Initialize with a value and validate the phone number
    def __init__(self, value):
        self.validate_phone(value) # Check if phone number is valid

        # Call the parent class constructor to set value
        super().__init__(value)
    
    # Validate if the phone number is exactly 10 digits
    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits.") # Raise error if invalid

# Birthday class inherits from Field, used for the birthdate
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(self.value)

# Record class represents a contact's information (name and phones)
class Record:
    # Initialize with a name and an empty list for phone numbers
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Add a phone number to the contact
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Remove a phone number from the contact
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # Edit an existing phone number
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
            else:
                print(f"Phone {old_phone} not found")
    
    # Find a specific phone number
    def find_phone(self, phone):
        return next((p for p in self.phones if p.value ==phone), None)
    
    # Add a birthday to the contact
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    # String representation of the contact (name and phone numbers)
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# AddressBook class is a container for storing contact records
class AddressBook(UserDict):
    # Add a contact's record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find a contact by name
    def find(self, name):
        return self.data.get(name, None)
    
    # Delete a contact by name
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Record for {name} not found ")
            
    # List of upcoming birthdays
    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        congratulation_list = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=current_date.year).date()

                if birthday_this_year < current_date:
                    birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)

                days_to_birthday = (birthday_this_year - current_date).days

                if 0 <= days_to_birthday < 7:
                    if birthday_this_year.weekday() >= 5:
                        days_to_birthday += (7 - birthday_this_year.weekday())

                    congratulation_date = current_date + timedelta(days=days_to_birthday)
                    congratulation_list.append({"name": record.name.value, "congratulation_date": congratulation_date.strftime("%Y.%m.%d")})

        return congratulation_list
