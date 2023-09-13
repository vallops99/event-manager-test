from enum import Enum


class CustomEnum(Enum):
    """Base of enums with get_vals method."""
    def __str__(self):
        return self.value

    @classmethod
    def get_vals(cls):
        """Get a list of the enum values."""
        return [x.value for x in cls]

    @classmethod
    def get_dict_vals(cls):
        """Get a dict of the enum values."""
        return {x.name: x.value for x in cls}
