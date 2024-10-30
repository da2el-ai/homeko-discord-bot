from .Settings import Settings


def debug_print(value):
    if Settings.debug:
        print(value)
        