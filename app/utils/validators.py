import re


def is_valid_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?[1-9]\d{7,14}$", phone))


def is_valid_pincode(pincode: str) -> bool:
    return bool(re.match(r"^\d{4,10}$", pincode))
