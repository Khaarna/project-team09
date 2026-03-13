import os
import pickle
import hashlib
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Set


# Models: phone_obj = Phone(phone) - исключения выбрасывает Phone

class Field: # value storage and interface
    
    def __init__(self, value: str):
         if value is None:
            raise ValueError("Value cannot be None")

        self._value = self.validate(value)

    def validate(self, value): # перевірка в дочірних класах
        return value

    @property
    def value(self): 
        return self._value # name.value як до атрибуту

    def show(self):
        return self._value
    
    def __str__(self): # формат друку 
        return str(self._value)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
            
        return self._value == other._value

    def __hash__(self): # використання value-obj як ключа в dict - Phone(str) = Name(str)
        return hash(self._value)

    #   return hash((type(self), self._value)) - для Phone(str) != Name(str)
   
class Name(Field): # value object
    
    def validate(self, value: str):
        if not value:            
            raise ValueError("Name cannot be empty.")
        return value

class Phone(Field): # value object

    def validate(self, value: str) -> str:
        value = value.strip()

        if value.startswith("+"):
            value = value[1:]

        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")

        return value

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value!r})"

class Address(Field):
    def validate(self, value:str) -> str:
        value = value.strip()

    if not value:
        raise ValueError("Address cannot be empty")  

        return value

class Email(Field):
    EMAIL_PATTERN = re.compile(r"^[^@\s]+@([\w-]+\.)+[A-Za-z]{2,}$")

    def validate(self, value: str) -> str:
        value = value.strip()
        if not self.EMAIL_PATTERN.fullmatch(value):
            raise ValueError("Invalid email format")
        return value

class Birthday(Field): #value onject
   
    def validate(self, value: str) -> date:
        value = value.strip()

        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")

    def next_birthday(self) -> date: # auxiliaries: part of Value Object (Birthday)'s logic
        today = date.today()

        try:
        next_bd = self.value.replace(year=today.year)
        except ValueError:
        next_bd = self.value.replace(year=today.year, day=28)

        if next_bd < today:        
            try:
                next_bd = next_bd.replace(year=today.year + 1)
            except ValueError:
                next_bd = next_bd.replace(year=today.year + 1, day=28)

        return next_bd

    def __str__(self):
        return self.value.strftime("%d.%m.%Y") 

class Tag(Field):
   
    def validate(self, value: str) -> str:
        if not value:
            raise ValueError("Tag cannot be empty")
        return value.lower().strip()  

class CRUDMixin:

    def _add_item(self, collection, cls, value):

        item = cls(value)

        if isinstance(collection, list):

            if item in collection:
                raise ValueError(f"{cls.__name__} already exists.")

            collection.append(item)
            return item

        if isinstance(collection, dict):

            if item.value in collection:
                raise ValueError(f"{cls.__name__} already exists.")

            collection[item.value] = item
            return item

    def _find_item(self, collection, cls, value):

        if isinstance(collection, list):

            for item in collection:
                if item.value == value:
                    return item
            return None

        if isinstance(collection, dict):

            key = cls(value).value
            return collection.get(key)

    def _remove_item(self, collection, cls, value):

        if isinstance(collection, list):

            item = self._find_item(collection, cls, value)

            if not item:
                raise ValueError(f"{cls.__name__} not found.")

            collection.remove(item)
            return

        if isinstance(collection, dict):

            key = cls(value).value

            if key not in collection:
                raise ValueError(f"{cls.__name__} not found.")

            del collection[key]   

    def _change_item(self, collection, cls, old_value, new_value):

        if isinstance(collection, list):

            item = self._find_item(collection, cls, old_value)

            if not item:
                raise ValueError(f"{cls.__name__} not found.")

            collection.remove(item)
            self._add_item(collection, cls, new_value)
            return

        if isinstance(collection, dict):

            old_key = cls(old_value).value

            if old_key not in collection:
                raise ValueError(f"{cls.__name__} not found.")

            new_item = cls(new_value)

            del collection[old_key]
            collection[new_item.value] = new_item     

class Note(CRUDMixin):

    def __init__(self, text: str):
        text = text.strip()

        if not text:
            raise ValueError("Note text cannot be empty.")

        self.text = text
        self._tags: dict[str, Tag] = {}
       
    @property
    def tags(self):
        return tuple(self._tags.values())

    def add_tag(self, value: str):
        self._add_item(self._tags, tag.value, tag)
        return tag

    def change_tag(self, old_value: str, new_value: str):
        self._change_item(self._tags, Tag(value), old_value, new_value)

    def remove_tag(self, value: str):
        self._remove_item(self._tags, Tag(value).value)

    def find_tag(self, value: str):
        return self._find_item(self._tags, Tag(value).value)

    def __str__(self):
        if not self._tags:
            return self.text
        return f"{self.text} [{', '.join(tag.value for tag in self._tags.values())}]"
    
    def has_tag(self, value: str):
        return Tag(value).value in self._tags    
    
# Aggregate Root:
   
class Record(CRUDMixin): # entity for Name and Phone storage; phone numbers add/delete
    def __init__(self, name: Name):
        if not isinstance(name, Name):
            raise TypeError("Expected Name instance.")
        self.name = name
        self._phones: list[Phone] = []
        self._emails: list[Email] = []
        self._addresses: list[Address] = []
        self.notes: list[Note] = []  
        self._birthday = None
 
    COLLECTIONS = {
        "phones": Phone,
        "emails": Email,
        "addresses": Address
    }

    @property
    def phones(self):
        return tuple(self._phones)

    @property
    def emails(self):
        return tuple(self._emails)

    @property
    def addresses(self):
        return tuple(self._addresses)

    @property
    def birthday(self):
        return self._birthday
    @property
    def all_tags(self):
        return {tag.name for note in self.notes for tag in note.tags}

    # common CRUD for value onjects:
    
    def _get_collection(self, field):
        return getattr(self, f"_{field}")

    def _set_birthday(self, birthday: Birthday | None, *, allow_override: bool = False):
        
        if birthday is not None and not isinstance(birthday, Birthday):
            raise TypeError("Expected Birthday instance")

        if birthday is not None and self._birthday is not None and not allow_override:
            raise ValueError("Birthday already exists")

        self._birthday = birthday

    # CRUD for COLLECTIONS:

    def add(self, field: str, value):
        collection = self._get_collection(field)
        cls = self.COLLECTIONS[field]

        return self._add_item(collection, cls, value)

    def find(self, field: str, value): 
        collection = self._get_collection(field)
        cls = self.COLLECTIONS[field]

        return self._find_item(collection, cls, value)


    def change(self, field: str, old_value, new_value):
        collection = self._get_collection(field)
        cls = self.COLLECTIONS[field]

        self._change_item(collection, cls, old_value, new_value)


    def remove(self, field: str, value):
        collection = self._get_collection(field)
        cls = self.COLLECTIONS[field]

        self._remove_item(collection, cls, value)

 # Auxiliary Business Logic for Birthdays

    def get_congratulation_date(self) -> datetime | None: 

        if not self.birthday:
            return None

        birthday_date = self.birthday.next_birthday()
       
        if birthday_date.weekday() == 5:  # Saturday
            birthday_date += timedelta(days=2)
        elif birthday_date.weekday() == 6:  # Sunday
            birthday_date += timedelta(days=1)

        return birthday_date

    def __str__(self):
        parts = [self.name.value]
        if self._phones:
            parts.append("Phones: " + ", ".join(p.value for p in self._phones))
        if self._emails:
            parts.append("Emails: " + ", ".join(e.value for e in self._emails))
        if self._addresses:
            parts.append("Addresses: " + ", ".join(a.value for a in self._addresses))
        if self.birthday: 
            parts.append(f"Birthday: {self.birthday}")
        return "; ".join(parts) if parts else self.name.value

 # Aggregate Collection/Repository            
                
class AddressBook(CRUDMixin):
    def __init__(self):
        self._records: dict[str, Record] = {}
        self._tag_index: dict[str, list[tuple[Record, Note]]] = {}

    @property
    def records(self):
        return tuple(self._records.values())

    def get_or_create_record(self, name: str) -> Record:

        key = name.lower()
        record = self._records.get(key)

        if record is None:
            record = Record(Name(name))
            self._records[key] = record
        
        return record

    def find(self, name: str):
        return self._records.get(name.lower())

    def delete(self, name: str):
        self._records.pop(name.lower(), None)
    
    def get_upcoming_birthdays(self, days_ahead: int = 7) -> list[dict]:

        today = date.today()
        upcoming = []

        for record in self._records.values():
            congratulation_date = record.get_congratulation_date()

            if congratulation_date is None:
                continue

            delta_days = (congratulation_date - today).days

            if 0 <= delta_days <= days_ahead:

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming

    # tag index:
     def index_tag(self, record: Record, note: Note):
        for tag in note.tags:
            self._tag_index.setdefault(tag.value, []).append((record, note))

    def remove_tag_index(self, record: Record, note: Note, tag: str):
        if tag in self._tag_index:
            self._tag_index[tag] = [
                (r, n) for r, n in self._tag_index[tag] if n is not note or r is not record
            ]
            if not self._tag_index[tag]:
                del self._tag_index[tag]

    def search_by_tag(self, tag: str):
        return self._tag_index.get(tag, [])

    def __iter__(self):
        return iter(self._records.values())

    def __str__(self):
        return "\n".join(str(record) for record in self)
        
# Dispatcher 

COMMANDS ={}

def command(name: str): # auto-adding functions into CONNABDS {}
    def decorator(func):

        if name in COMMANDS:
            raise ValueError(f"Command '{name}' already registered")
            
        COMMANDS[name] = func
        return func
    return decorator

def dispatch_command(command: str, args: list[str], book: AddressBook) -> str:

    handler = COMMANDS.get(command)

    if handler is None:
        return "Unknown command."

    try:
        return handler(args, book)

    except Exception as e:
        return str(e)

# Application Layer: commands

def input_error(func): # auxiliaries: декоратор обробки помилок
    def inner(args, book):
        try:
            return func(args, book)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments."
    return inner

# commands registration for collections:
def register_crud_commands(entity: str, field: str):

    @command(f"add-{entity}")
    @input_error
    def add_item(args, book):
        name, value = args

        record = book.get_or_create_record(name)
        record.add(field, value)

        return f"{entity.capitalize()} added."

    @command(f"change-{entity}")
    @input_error
    def change_item(args, book):
        name, old_value, new_value = args

        record = book.find(name)
        if not record:
            return "Contact not found"

        record.change(field, old_value, new_value)

        return f"{entity.capitalize()} updated."

    @command(f"remove-{entity}")
    @input_error
    def remove_item(args, book):
        name, value = args

        record = book.find(name)
        if not record:
            return "Contact not found"

        record.remove(field, value)

        return f"{entity.capitalize()} removed."

    @command(f"show-{field}")
    @input_error
    def show_items(args, book):
        name = args[0]

        record = book.find(name)
        if not record:
            return "Contact not found"

        items = getattr(record, field)

        return ", ".join(i.value for i in items) if items else f"No {field}"

# commands registration for birthday:
def register_birthday_commands():

    @command("add-birthday")
    @input_error
    def add_birthday(args, book):
        name, value = args
        record = book.get_or_create_record(name)

        record._set_birthday(Birthday(value))

        return "Birthday added."

    @command("change-birthday")
    @input_error
    def change_birthday(args, book):
        name, value = args

        record = _get_record(book, name)
        record._set_birthday(Birthday(value), allow_override=True)

        return "Birthday updated."

    @command("remove-birthday")
    @input_error
    def remove_birthday(args, book):
        name = args[0]

        record = _get_record(book, name)
        record._set_birthday(None, allow_override=True)

        return "Birthday removed."


    @command("show-birthday")
    @input_error
    def show_birthday(args, book):
        name = args[0]

        record = _get_record(book, name)

        return str(record.birthday) if record.birthday else "Birthday not set"

# commands registration for notes and tags:
def register_note_tag_commands():

    def _get_note(book, name, index):
        record = _get_record(book, name)
        return record, record.notes[int(index)]


    @command("add-tag")
    @input_error
    def add_tag(args, book):
        name, index, tag = args

        record, note = _get_note(book, name, index)

        note.add_tag(tag)
        book.index_tag(record, note)

        return "Tag added."


    @command("remove-tag")
    @input_error
    def remove_tag(args, book):
        name, index, tag = args

        record, note = _get_note(book, name, index)

        note.remove_tag(tag)
        book.remove_tag_index(record, note, tag)

        return "Tag removed."


    @command("search-tag")
    @input_error
    def search_tag(args, book):

        tag = args[0]
        results = book.search_by_tag(tag)

        if not results:
            return "No notes found."

        return "\n".join(f"{name}: {note.text}" for name, note in results)
        
# Initialization:        

register_birthday_commands()

register_note_tag_commands()

for field in Record.COLLECTIONS:
    entity = field[:-1]  # phones -> phone
    register_collection_commands(field)

# Парсер: команда (на першому місці) + аргумент(и) (для деяких команд відсутній)

def parse_input(user_input: str) -> tuple[str, list[str]]:
    user_input = user_input.strip()

    if not user_input:
        raise ValueError("Empty input.")

    parts = user_input.split()

    command = parts[0].lower()   
    args = parts[1:]             

    return command, args

# Infrastructure: pickle (load with data integrity check/save)

def load_data(filename="addressbook.pkl", hash_filename="addressbook.hash"):
    try:
        with open(filename, "rb") as f:
            data_bytes = f.read()

        with open(hash_filename, "r") as f:
            saved_hash = f.read().strip()

        current_hash = hashlib.sha256(data_bytes).hexdigest()

        if current_hash != saved_hash:
            raise ValueError("Data integrity check failed! File corrupted.")

        return pickle.loads(data_bytes)

    except (FileNotFoundError, AttributeError, pickle.UnpicklingError):
        return AddressBook()


def save_data(book, filename="addressbook.pkl", hash_filename="addressbook.hash"):

    data_bytes = pickle.dumps(book)
    temp_file = filename +'.tmp' # file spoilage preventing

    with open(temp_file, "wb") as f:
        f.write(data_bytes)

    os.replace(temp_file, filename)

    file_hash = hashlib.sha256(data_bytes).hexdigest()

    with open(hash_filename, "w") as f:
        f.write(file_hash)

# CLI (input, print) 

def main(): 

    book = load_data()

    print("Welcome to the assistant bot!")
    print(
"""Available commands:

  hello
  add 
  change
  phone
  all
  add-birthday
  show-birthday
  birthdays
  close
  exit

"""
)
    while True:
        user_input = input(">>> ")

        try:
            command, args = parse_input(user_input)

            if command in ("exit", "close"):
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")
                continue

            else:
                result = dispatch_command(command, args, book)
                print(result)

        except ValueError as e:
            print(e)

    save_data(book)

if __name__ == "__main__":
    main()