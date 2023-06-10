from enum import Enum, auto, unique


@unique
class UnlockTypes(Enum):
    block = auto()
    entity = auto()
    item = auto()


@unique
class SupportedTypes(Enum):
    block = auto()
    brewing = auto()
    entity = auto()
    item = auto()
    mining = auto()
    smithing = auto()
    crafting = auto()

    # advancements = auto()
    # tags = auto()

    @classmethod
    def get_by(cls, value: str | int):
        return getattr(cls, value, cls(int(value)))


@unique
class AvailableSkills(Enum):
    health = auto()
    strength = auto()
    agility = auto()
    defense = auto()
    stamina = auto()
    luck = auto()
    archery = auto()
    trade = auto()
    smithing = auto()
    mining = auto()
    farming = auto()
    alchemy = auto()

    @classmethod
    def get_by(cls, value: str | int):
        return getattr(cls, value, cls(int(value)))
