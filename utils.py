import re

def is_strong_password(password):
    """Check if password meets complexity requirements."""
    if len(password) < 8:
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[^a-zA-Z0-9]', password):  # special char
        return False
    return True
