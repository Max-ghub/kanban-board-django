import random


def generate_phone_code():
    """Генерация SMS кода"""
    return str(random.randint(100000, 999999))
