from address_book import AddressBook, Record

# Input error handler.
def input_error(error_message=None):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError):
                return error_message
            except KeyError:
                return error_message or "Contact not found"
        return inner
    return decorator

# Parse user input.
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# Add new contact.
@input_error("Please enter the 'add' command with [name] [phone].")
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    if record is not None:
        return "Contact already exist, please enter different name."
    record = Record(name)
    book.add_record(record)
    record.add_phone(phone)
    
    return "Contact added."

# Change existing contact.
@input_error("Please enter the 'change' command with [name] [old_phone] [new_phone].")
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."

# Show phone for requested user.
@input_error("Please enter the 'phone' command with [name].")
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(p.value for p in record.phones)}"
    return "Contact not found."

# Show all contacts.
def show_all_contacts(book):
    if not book.data:
        return "No contacts available."
    return "\n".join([str(record) for record in book.data.values()])

# Add birthday to a contact.
@input_error("Please enter the 'add-birthday' command with [name] [birthday].")
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

# Show birthday for requested user.
@input_error("Please enter the 'show-birthday' command with [name].")
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Contact or birthday not found."

# Show birthdays for the next week.
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    return "\n".join([f"{entry['name']} - {entry['congratulation_date']}" for entry in upcoming_birthdays])

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()