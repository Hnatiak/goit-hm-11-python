from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value=None):
        if value and not self.is_valid_birthday(value):
            raise ValueError("Invalid birthday format")
        super().__init__(value)

    @staticmethod
    def is_valid_birthday(value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        if Phone.is_valid_phone(phone):
            self.phones.append(Phone(phone))
        else:
            raise ValueError("Invalid phone number format")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        if Phone.is_valid_phone(new_phone):
            for p in self.phones:
                if p.value == old_phone:
                    p.value = new_phone
                    return
            raise ValueError("Old phone number not found")
        else:
            raise ValueError("Invalid new phone number format")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # def days_to_birthday(self):
    #     if self.birthday.value:
    #         today = datetime.today()
    #         # next_birthday = datetime(today.year, *map(int, self.birthday.value.split('-')))
    #         next_birthday = datetime(today.year, map(int, self.birthday.value.split('-')))
    #         if today > next_birthday:
    #             next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split('-')))
    #         return (next_birthday - today).days
    #     return None
    
    # def days_to_birthday(self):
    #     if self.birthday and self.birthday.value:
    #         today = datetime.today()
    #         next_birthday = datetime(today.year, *map(int, self.birthday.value.split('-')))
    #         if today > next_birthday:
    #             next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split('-')))
    #         return (next_birthday - today).days
    #     return None
    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today()
            date_parts = self.birthday.value.split('-')
            print("Date parts:", date_parts)  # Add this line for debugging
            next_birthday = datetime(today.year, *map(int, date_parts))
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, date_parts))
            return (next_birthday - today).days
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i + n]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def main():
    book = AddressBook()

    john_record = Record("John", "1990-05-15")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane", "1985-08-20")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")

    print(f"Days to John's next birthday: {john.days_to_birthday()}")

    N = 1
    for page_num, page_records in enumerate(book.iterator(N), start=1):
        print(f"\nPage {page_num}:")
        for record in page_records:
            print(record)


if __name__ == "__main__":
    main()