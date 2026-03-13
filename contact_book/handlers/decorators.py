def input_error(func):
    """Decorator that catches common input errors and returns friendly messages."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Error: {e.args[0]}"
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Invalid command format. Missing arguments."
    return inner
