from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(value):
    if not value.isalpha():
        raise ValidationError(_("Ism faqat harflar iborat bolishi kerak"))
    if len(value) < 3:
        raise ValidationError(_("Ism 3 ta simvoldan kop bo'lishi keral"))


def validate_description(value):
    if len(value) < 10:
        raise ValidationError(_("Tavsifi kamida 10 simvoldan koproq bolishi kerak"))


def validate_price(value):
    if value <= 0:
        raise ValidationError(_("Narx musbat son bolishi shart!!"))


def validate_quantity(value):
    if value < 0:
        raise ValidationError(_("Soni musbat son bolishi shart"))


def validate_email(value):
    if "@" not in value or "." not in value.split("@")[-1]:
        raise ValidationError(_("Pochtangizni tog'ri kriting"))


def validate_password(value):
    if len(value) < 8:
        raise ValidationError(_("Parol 8 ta simvoldan koproq bolishi shart"))
    if not any(char.isdigit() for char in value):
        raise ValidationError(_("Parolni ichida kamida 1 ta son bolishi kerak"))
    if not any(char.isalpha() for char in value):
        raise ValidationError(_("Parolni ichida kamida bitta harf bolishi kerak"))
