from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^\+?\d{10,12}$",
    message="Номер телефона должен содержать от 10 до 12 цифр и может начинаться с '+'",
)
