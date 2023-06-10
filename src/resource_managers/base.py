from abc import abstractmethod
from pathlib import Path

from src.enums import AvailableSkills, SupportedTypes
from src.support import InputData


def get_skills_info():
    return '\n\t\t-> '.join([f'{item.value}. {item.name}' for item in AvailableSkills])


def get_types_info():
    return '\n\t'.join([f'{item.value}. {item.name}' for item in SupportedTypes])


class ResourceManager:

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.previous_skill: AvailableSkills | None = None

    @abstractmethod
    def add_object(self, mod_id: str, object_id: str, skill: AvailableSkills, level: int | None = None):
        raise NotImplementedError

    @property
    @abstractmethod
    def base_dict(self) -> dict[str, any]:
        raise NotImplementedError

    def user_input(
        self, previous_mod_id: str | None, previous_skill: AvailableSkills, previous_level: int | None
    ) -> InputData:
        if previous_mod_id is None:
            mod_id = None
            while not mod_id:
                mod_id = input('Mod id\n> ')
        else:
            mod_id = input(
                f'Mod id\n\t-> Previous mod_id: <{previous_mod_id}>\n\tLeave blank for use previous value\n> ')

        item_id = input('Item ID:\n> ')
        if previous_skill is None:
            skill = None
            while not skill:
                skill = input(f'Skill:\n\t-> Available values (use number or name):\n\t\t-> {get_skills_info()}\n> ')
                if not skill:
                    continue
                skill = AvailableSkills.get_by(skill)
        else:
            skill = input(
                f'Skill:\n\t-> Available values (use number or name):\n\t\t-> {get_skills_info()}'
                f'\n\t-> Previous: <{previous_skill.name}>\n\tLeave blank for previous value\n> '
            )
            if skill:
                skill = AvailableSkills.get_by(skill)

        if skill != self.previous_skill:
            self.previous_skill = skill

        if previous_level is None:
            level = None
            while not level:
                level = input(f'Item level:\n> ')
        else:
            level = input(f'Item level:\n\t-> Previous: <{previous_level}>\n\tLeave blank for previous value\n> ')
        return InputData(mod_id or previous_mod_id, item_id, previous_skill, level or previous_level)
