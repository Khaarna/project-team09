"""Test suite for the Contact Book Assistant."""

import sys

from contact_book.models import AddressBook, NotesBook
from contact_book.handlers import dispatch_command
from contact_book.handlers.dispatcher import CONTACT_COMMANDS
from contact_book.storage import AppContext


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ctx() -> AppContext:
    """Fresh in-memory AppContext for each test."""
    return AppContext(AddressBook(), NotesBook())


def _ok(label: str) -> None:
    print(f"  ✓ {label}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_contact_core():
    ctx = _ctx()

    r = dispatch_command("add", ["John"], ctx)
    assert "added" in r.lower()
    _ok("add contact")

    dispatch_command("add-phone", ["John", "1234567890"], ctx)
    dispatch_command("add-phone", ["John", "0987654321"], ctx)
    r = dispatch_command("show-phones", ["John"], ctx)
    assert "1234567890" in r and "0987654321" in r
    _ok("add-phone / show-phones")

    r = dispatch_command("change-phone", ["John", "1", "1112223333"], ctx)
    assert "updated" in r.lower()
    r = dispatch_command("show-phones", ["John"], ctx)
    assert "1112223333" in r and "1234567890" not in r
    _ok("change-phone by index")

    r = dispatch_command("info", ["John"], ctx)
    assert r is None  # rendered directly
    assert ctx.book.find("John") is not None
    _ok("info (rich render)")

    r = dispatch_command("add-birthday", ["John", "01.01.1990"], ctx)
    assert "added" in r.lower()
    r = dispatch_command("show-birthday", ["John"], ctx)
    assert "01.01.1990" in r
    _ok("add-birthday / show-birthday")

    r = dispatch_command("birthdays", ["365"], ctx)
    assert r is not None
    _ok("birthdays")

    dispatch_command("all", [], ctx)          # rich render, no assertion needed
    _ok("all (rich render)")

    results = ctx.book.search("John")
    assert len(results) > 0
    _ok("book.search")

    r = dispatch_command("delete", ["John"], ctx)
    assert "deleted" in r.lower()
    assert ctx.book.find("John") is None
    _ok("delete contact")


def test_dynamic_commands_registered():
    for cmd in (
        "add-phone", "change-phone", "remove-phone", "show-phones",
        "add-email", "change-email", "remove-email", "show-emails",
        "add-address", "change-address", "remove-address", "show-addresses",
    ):
        assert cmd in CONTACT_COMMANDS, f"'{cmd}' not registered"
        _ok(f"{cmd} registered")


def test_add_commands():
    ctx = _ctx()

    r = dispatch_command("add-phone", ["Alice", "1234567890"], ctx)
    assert "added" in r.lower()
    r = dispatch_command("add-email", ["Alice", "alice@example.com"], ctx)
    assert "added" in r.lower()

    record = ctx.book.find("Alice")
    assert len(record.phones) == 1
    assert len(record.emails) == 1
    _ok("add-phone + add-email")


def test_show_commands():
    ctx = _ctx()
    dispatch_command("add-phone", ["Bob", "1112223333"], ctx)
    dispatch_command("add-phone", ["Bob", "4445556666"], ctx)
    dispatch_command("add-email", ["Bob", "bob@test.com"], ctx)
    dispatch_command("add-email", ["Bob", "bob2@test.com"], ctx)

    r = dispatch_command("show-phones", ["Bob"], ctx)
    assert "1112223333" in r and "4445556666" in r
    _ok("show-phones")

    r = dispatch_command("show-emails", ["Bob"], ctx)
    assert "bob@test.com" in r and "bob2@test.com" in r
    _ok("show-emails")


def test_change_commands():
    ctx = _ctx()
    dispatch_command("add-phone", ["Charlie", "1234567890"], ctx)
    dispatch_command("add-email", ["Charlie", "charlie@old.com"], ctx)

    r = dispatch_command("change-phone", ["Charlie", "1", "0987654321"], ctx)
    assert "updated" in r.lower()
    r = dispatch_command("show-phones", ["Charlie"], ctx)
    assert "0987654321" in r and "1234567890" not in r
    _ok("change-phone")

    r = dispatch_command("change-email", ["Charlie", "1", "charlie@new.com"], ctx)
    assert "updated" in r.lower()
    r = dispatch_command("show-emails", ["Charlie"], ctx)
    assert "charlie@new.com" in r and "charlie@old.com" not in r
    _ok("change-email")


def test_remove_commands():
    ctx = _ctx()
    dispatch_command("add-phone", ["David", "1112223333"], ctx)
    dispatch_command("add-phone", ["David", "4445556666"], ctx)
    dispatch_command("add-email", ["David", "david@test.com"], ctx)

    r = dispatch_command("remove-phone", ["David", "1"], ctx)
    assert "removed" in r.lower()
    assert len(ctx.book.find("David").phones) == 1
    _ok("remove-phone")

    r = dispatch_command("remove-email", ["David", "1"], ctx)
    assert "removed" in r.lower()
    assert len(ctx.book.find("David").emails) == 0
    _ok("remove-email")


def test_error_handling():
    ctx = _ctx()
    dispatch_command("add-phone", ["Eve", "1234567890"], ctx)

    r = dispatch_command("add-phone", ["Eve", "1234567890"], ctx)
    assert "already exists" in r.lower()
    _ok("duplicate prevention")

    r = dispatch_command("change-phone", ["NoOne", "1", "0000000000"], ctx)
    assert "not found" in r.lower()
    _ok("contact not found")

    r = dispatch_command("remove-phone", ["Eve", "99"], ctx)
    assert "out of range" in r.lower()
    _ok("index out of range")


def test_note_commands():
    ctx = _ctx()

    r = dispatch_command("add-note", ["MyNote", "some", "content"], ctx)
    assert "added" in r.lower()
    _ok("add-note")

    r = dispatch_command("note", ["MyNote"], ctx)
    assert r is None  # rich render
    _ok("note (rich render)")

    r = dispatch_command("edit-note", ["MyNote", "updated", "content"], ctx)
    assert "updated" in r.lower()
    _ok("edit-note")

    r = dispatch_command("add-tag", ["MyNote", "work"], ctx)
    assert "added" in r.lower()
    _ok("add-tag")

    r = dispatch_command("search-tag", ["work"], ctx)
    assert r is None  # rich render
    _ok("search-tag (rich render)")

    r = dispatch_command("remove-tag", ["MyNote", "work"], ctx)
    assert "removed" in r.lower()
    _ok("remove-tag")

    dispatch_command("notes", [], ctx)
    _ok("notes (rich render)")

    r = dispatch_command("search-notes", ["updated"], ctx)
    assert r is None  # rich render
    _ok("search-notes (rich render)")

    r = dispatch_command("delete-note", ["MyNote"], ctx)
    assert "deleted" in r.lower()
    _ok("delete-note")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

TESTS = [
    test_contact_core,
    test_dynamic_commands_registered,
    test_add_commands,
    test_show_commands,
    test_change_commands,
    test_remove_commands,
    test_error_handling,
    test_note_commands,
]

if __name__ == "__main__":
    passed = failed = 0
    for fn in TESTS:
        print(f"\n{'─' * 50}")
        print(f"  {fn.__name__.replace('_', ' ').title()}")
        print(f"{'─' * 50}")
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            import traceback; traceback.print_exc()
            failed += 1

    print(f"\n{'=' * 50}")
    if failed == 0:
        print(f"  ✓✓✓  ALL {passed} TESTS PASSED")
    else:
        print(f"  {passed} passed, {failed} FAILED")
    print(f"{'=' * 50}\n")
    sys.exit(1 if failed else 0)
