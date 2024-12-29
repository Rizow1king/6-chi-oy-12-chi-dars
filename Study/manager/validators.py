from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError('Bu maydon faqat harflar va bo‘sh joylardan iborat bo‘lishi kerak.')


def validate_email(value):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, value):
        raise ValidationError('Iltimos, to‘g‘ri email manzilini kiriting.')


def validate_password_strength(value):
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Parolda kamida bitta katta harf bo‘lishi kerak.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('Parolda kamida bitta raqam bo‘lishi kerak.')
    if not re.search(r'[@$!%*?&]', value):
        raise ValidationError('Parolda kamida bitta maxsus belgidan biri bo‘lishi kerak.')
    if len(value) < 8:
        raise ValidationError('Parol kamida 8 ta belgidan iborat bo‘lishi kerak.')


def validate_homework(value):
    if len(value) < 10:
        raise ValidationError('Uyga vazifa kamida 10 ta belgidan iborat bo‘lishi kerak.')


def validate_description(value):
    if len(value) < 20:
        raise ValidationError('Tavsif kamida 20 ta belgidan iborat bo‘lishi kerak.')
    if len(value) > 1000:
        raise ValidationError('Tavsif 1000 ta belgidan oshmasligi kerak.')
