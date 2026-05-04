from django.core.exceptions import ValidationError


def validators_username(value):
    for char in value:
        if not char.isalnum() and char != '_':
            raise ValidationError("Уверете се, че тази стойност съдържа само букви, цифри и подчертаване.")

