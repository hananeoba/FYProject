import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:  # BaseValidator:
    def __init__(self, min_length=15):
        self.min_length = min_length
        self.special_chars = "$£#^~"

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long."
            )

        if not any(char.islower() for char in value):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not any(char.isupper() for char in value):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one digit.")

        if not any(char in self.special_chars for char in value):
            raise ValidationError(
                "Password must contain at least one of the following special characters: $ £ # ^ ~"
            )



def is_kernel(user):
    if (user.is_superuser):
        return True
    if (user.company is None):
        return False
    return (user.company.code.lower() == "root" and user.is_superuser)

class CustomUserValidator:
    @staticmethod
    def validate_char_field(value):
        pattern = r'^[a-zA-Z0-9_]$'  # Regular expression pattern to match valid characters
        if re.match(pattern, value):
            return value
        else:
            raise ValidationError('Invalid character in field')  # Raise ValidationError if validation fails
