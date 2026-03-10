from collections import UserDict
from datetime import datetime, timedelta, date

from .record import Record


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        pass

    def search(self, query):
        pass

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming = []

        def birthday_in_year(bday, year):
            try:
                return bday.replace(year=year)
            except ValueError:
                return date(year, 3, 1)  # Feb 29 → Mar 1 in non-leap years

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            upcoming_birthday = birthday_in_year(birthday, today.year)
            if upcoming_birthday < today:
                upcoming_birthday = birthday_in_year(birthday, today.year + 1)

            days_until = (upcoming_birthday - today).days
            if 0 <= days_until <= days:
                if upcoming_birthday.weekday() == 5:
                    congratulation_date = upcoming_birthday + timedelta(days=2)
                elif upcoming_birthday.weekday() == 6:
                    congratulation_date = upcoming_birthday + timedelta(days=1)
                else:
                    congratulation_date = upcoming_birthday

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    "days_until": days_until,
                })

        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming
