from models import NotesBook
from .decorators import input_error
from .dispatcher import note_command


@note_command("add-note")
@input_error
def add_note(args, notes: NotesBook):
    if len(args) < 1:
        return "Usage: add-note <title> <content>"
    title = args[0]
    content = " ".join(args[1:]) if len(args) > 1 else ""
    notes.add(title, content)
    return "Note added."


@note_command("note")
@input_error
def show_note(args, notes: NotesBook):
    if len(args) < 1:
        return "Usage: note <title>"
    return str(notes.find(args[0]))


@note_command("edit-note")
@input_error
def edit_note(args, notes: NotesBook):
    if len(args) < 2:
        return "Usage: edit-note <title> <content>"
    title = args[0]
    new_content = " ".join(args[1:])
    notes.edit(title, new_content)
    return "Note updated."


@note_command("delete-note")
@input_error
def delete_note(args, notes: NotesBook):
    if len(args) < 1:
        return "Usage: delete-note <title>"
    title = args[0]
    notes.delete(title)
    return f"Note '{title}' deleted."


@note_command("notes")
@input_error
def show_all_notes(args, notes: NotesBook):
    return notes.all()


@note_command("search-notes")
@input_error
def search_notes(args, notes: NotesBook):
    if len(args) < 1:
        return "Usage: search-notes <query>"
    query = " ".join(args)
    found_notes = notes.search(query)
    if not found_notes:
        return f"No notes found for '{query}'."
    return "\n\n".join(str(note) for note in found_notes)


@note_command("add-tag")
@input_error
def add_tag(args, notes: NotesBook):
    if len(args) < 2:
        return "Usage: add-tag <title> <tag>"
    title, tag = args[0], args[1]
    notes.add_tag(title, tag)
    return "Tag added."


@note_command("remove-tag")
@input_error
def remove_tag(args, notes: NotesBook):
    if len(args) < 2:
        return "Usage: remove-tag <title> <tag>"
    title, tag = args[0], args[1]
    notes.remove_tag(title, tag)
    return "Tag removed."


@note_command("search-tag")
@input_error
def search_by_tag(args, notes: NotesBook):
    if len(args) < 1:
        return "Usage: search-tag <tag>"
    tag = args[0]
    found_notes = notes.search_by_tag(tag)
    if not found_notes:
        return f"No notes found with tag '{tag}'."
    return "\n\n".join(str(note) for note in found_notes)
