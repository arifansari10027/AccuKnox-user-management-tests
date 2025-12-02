import random
import string

# Existing employee name (used for auto-suggest in Employee Name field)
# We only need a part of the name that appears in the dropdown.
EMPLOYEE_NAME = "a"


def unique_username(prefix: str = "arif_exe_") -> str:
    """
    Generate a unique username each time so we don't clash with existing users.
    Example: arif_exe_a1b2c3d4
    """
    suffix = "".join(random.choices("0123456789abcdef", k=8))
    return f"{prefix}{suffix}"
