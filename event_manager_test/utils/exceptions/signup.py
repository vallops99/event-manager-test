from rest_framework.exceptions import ValidationError


class SignUpPasswordException(ValidationError):
    default_detail = "Passwords do not match!"
