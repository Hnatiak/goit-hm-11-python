from datetime import datetime
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
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.is_valid_phone(new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value

    @staticmethod
    def is_valid_phone(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value is not None and not self.is_valid_birthday(new_value):
            raise ValueError("Invalid birthday format")
        self._value = new_value

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
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Old phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if not self.birthday.value:
            raise ValueError("Please, add birthday firstly")

        today = datetime.now().date()
        birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()

        next_birthday_year = today.year

        if today.month > birthday_date.month or (today.month == birthday_date.month and today.day > birthday_date.day):
            next_birthday_year += 1

        next_birthday = datetime(
            year=next_birthday_year,
            month=birthday_date.month,
            day=birthday_date.day
        )

        return (next_birthday.date() - today).days

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