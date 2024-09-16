import enum


class AutoNamedEnum(enum.Enum):
    """
    USAGE:

    ```python
    from enum import auto

    from app.core.enums import AutoNamedEnum

    class Color(AutoNamedEnum):
        RED = auto()
        GREEN = auto()
        BLUE = auto()

    ```
    """

    def _generate_next_value_(name, start, count, last_values) -> str:
        return name


class EnumBuilder:
    @staticmethod
    def create_enum(class_name, languages):
        languages_dict = {lang: lang.upper() for lang in languages}
        return enum.Enum(class_name, languages_dict)
