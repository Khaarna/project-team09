import os
import hashlib
import pickle

from .models import AddressBook, NotesBook

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA_FILE = os.path.join(_DATA_DIR, "data.pkl")
HASH_FILE = os.path.join(_DATA_DIR, "data.hash")


class AppContext:
    """Holds application state and manages persistence."""

    def __init__(self, book: AddressBook, notes: NotesBook):
        self.book = book
        self.notes = notes

    def save(self, filename: str = DATA_FILE, hash_filename: str = HASH_FILE) -> None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        data_bytes = pickle.dumps({"book": self.book, "notes": self.notes})
        temp_file = filename + ".tmp"
        with open(temp_file, "wb") as f:
            f.write(data_bytes)
        os.replace(temp_file, filename)
        with open(hash_filename, "w") as f:
            f.write(hashlib.sha256(data_bytes).hexdigest())

    @classmethod
    def load(cls, filename: str = DATA_FILE, hash_filename: str = HASH_FILE) -> "AppContext":
        try:
            with open(filename, "rb") as f:
                data_bytes = f.read()
            with open(hash_filename, "r") as f:
                saved_hash = f.read().strip()
            if hashlib.sha256(data_bytes).hexdigest() != saved_hash:
                print("Warning: data integrity check failed. Starting fresh.")
                return cls(AddressBook(), NotesBook())
            data = pickle.loads(data_bytes)
            return cls(data["book"], data["notes"])
        except FileNotFoundError:
            return cls(AddressBook(), NotesBook())
        except (AttributeError, pickle.UnpicklingError, KeyError):
            print("Warning: could not load data. Starting fresh.")
            return cls(AddressBook(), NotesBook())
