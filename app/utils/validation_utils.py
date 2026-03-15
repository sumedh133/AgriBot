import re

def validate_email(email: str):
    if not email:
        return False, "Email is required"

    email = email.strip().lower()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        return False, "Invalid email format"

    return True, None


def validate_password(password: str):
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    return True, None