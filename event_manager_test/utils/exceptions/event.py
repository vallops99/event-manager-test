from rest_framework.exceptions import ValidationError, PermissionDenied


class BadStartDatetimeError(ValidationError):
    default_detail = "Start date must be tomorrow or later!"


class BadEndDatetimeError(ValidationError):
    default_detail = "End date must be after start date!"


class UserAlreadyRegisteredError(ValidationError):
    default_detail = "You are already registered to this event!"


class UserNotRegisteredYetError(ValidationError):
    default_detail = "You are not registered to this event yet!"


class MaxEventCapacityError(ValidationError):
    default_detail = "Maximum value of registered user reached!"


class MustBeTheOwnerError(PermissionDenied):
    default_detail = "You must be the owner of the event to make changes!"


class PastEventRegistrationError(ValidationError):
    default_detail = "You can not register to a past event!"
