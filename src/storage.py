import os
import pickle

from models import AddressBook, NotesBook

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.pkl")


def save_data(book: AddressBook, notes: NotesBook, filename: str = DATA_FILE):
    with open(filename, "wb") as f:
        pickle.dump({"book": book, "notes": notes}, f)


def load_data(filename: str = DATA_FILE):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return data["book"], data["notes"]
    except FileNotFoundError:
        return AddressBook(), NotesBook()
