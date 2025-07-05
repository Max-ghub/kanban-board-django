from celery import shared_task

from .models import PhoneCode
from .services import generate_phone_code


@shared_task()
def send_phone_code_task(phone):
    code = generate_phone_code()
    PhoneCode.create_phone_code(phone, code)
    print(f"[INFO] Отправлен код {code} на номер {phone}")
