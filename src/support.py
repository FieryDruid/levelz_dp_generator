from typing import NamedTuple

from src.enums import AvailableSkills


class InputData(NamedTuple):
    mod_id: str
    object_id: str
    skill: AvailableSkills | None
    level: int | None
