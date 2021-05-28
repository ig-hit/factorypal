import enum


class ChoiceEnum(enum.Enum):
    @classmethod
    def as_choices(cls, reverse=False):
        return [(tag.value, tag.name) if reverse else (tag.name, tag.value) for tag in cls]

    @classmethod
    def names(cls):
        return [tag.name for tag in cls]

    @classmethod
    def values(cls):
        return [tag.value for tag in cls]
