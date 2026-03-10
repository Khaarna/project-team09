from models import NotesBook
from .decorators import input_error


@input_error
def add_note(args, notes: NotesBook):
    pass


@input_error
def show_note(args, notes: NotesBook):
    pass


@input_error
def edit_note(args, notes: NotesBook):
    pass


@input_error
def delete_note(args, notes: NotesBook):
    pass


@input_error
def show_all_notes(notes: NotesBook):
    pass


@input_error
def search_notes(args, notes: NotesBook):
    pass


@input_error
def add_tag(args, notes: NotesBook):
    pass


@input_error
def remove_tag(args, notes: NotesBook):
    pass


@input_error
def search_by_tag(args, notes: NotesBook):
    pass
