from models import NotesBook
from .decorators import input_error
from .dispatcher import note_command


@note_command("add-note")
@input_error
def add_note(args, notes: NotesBook):
    pass


@note_command("note")
@input_error
def show_note(args, notes: NotesBook):
    pass


@note_command("edit-note")
@input_error
def edit_note(args, notes: NotesBook):
    pass


@note_command("delete-note")
@input_error
def delete_note(args, notes: NotesBook):
    pass


@note_command("notes")
@input_error
def show_all_notes(args, notes: NotesBook):
    pass


@note_command("search-notes")
@input_error
def search_notes(args, notes: NotesBook):
    pass


@note_command("add-tag")
@input_error
def add_tag(args, notes: NotesBook):
    pass


@note_command("remove-tag")
@input_error
def remove_tag(args, notes: NotesBook):
    pass


@note_command("search-tag")
@input_error
def search_by_tag(args, notes: NotesBook):
    pass
