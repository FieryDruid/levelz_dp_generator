import json
from pathlib import Path

from src.enums import AvailableSkills, SupportedTypes
from src.resource_managers.base import ResourceManager
from src.resource_managers.multiple import ProfessionBlocksManager, ProfessionItemsManager
from src.resource_managers.single import BlockUnlockManager, EntityUnlockManager, ItemUnlockManager
from src.support import InputData

mcmeta_content = {
    'pack': {
        'pack_format': 0,
        'description': ''
    }
}


class DatapackConstructor:

    def __init__(self, pack_format: int, pack_name: str | None = None, description: str | None = None) -> None:
        self.base_path = Path.cwd()
        pack_name: str = pack_name or 'MoreLevelZ'
        main_folder = self.base_path / pack_name
        main_folder.mkdir(parents=True, exist_ok=True)

        mcmeta_file = main_folder / 'pack.mcmeta'
        mcmeta_content['pack']['pack_format'] = pack_format
        mcmeta_content['pack']['description'] = description or ''
        with mcmeta_file.open('w') as file:
            json.dump(mcmeta_content, file, indent=4)
        self.levelz_folders = main_folder / 'data' / 'levelz'
        self._make_for = None
        self.resource_manager: type[ResourceManager] | None = None
        self.previous_level = 0
        self.previous_skill = AvailableSkills.smithing
        self.previous_mod_id = None
        self.managers: dict[SupportedTypes, ResourceManager] = {}

    @property
    def active_manager(self) -> ResourceManager:
        return self.managers[self.make_for]

    @property
    def make_for(self) -> SupportedTypes:
        if not self._make_for:
            raise ValueError('Set value before use')
        return self._make_for

    @make_for.setter
    def make_for(self, value: SupportedTypes):
        if not isinstance(value, SupportedTypes):
            raise TypeError('Unsupported value for attr "make_for"')
        self._make_for = value
        if value not in self.managers:
            match value:
                case SupportedTypes.block:
                    manager = BlockUnlockManager
                case SupportedTypes.entity:
                    manager = EntityUnlockManager
                case SupportedTypes.mining:
                    manager = ProfessionBlocksManager
                case SupportedTypes.item:
                    manager = ItemUnlockManager
                case SupportedTypes.brewing | SupportedTypes.smithing:
                    manager = ProfessionItemsManager
                case _:
                    raise NotImplementedError(f'Unsupported type {value}')
            type_path = self.levelz_folders / value.name
            self.managers[value] = manager(type_path)

    def input(self) -> InputData:
        return self.active_manager.user_input(self.previous_mod_id, self.previous_skill, self.previous_level)

    def add(self, mod_id: str | None, item_id: str, skill: AvailableSkills | None, level: int | str | None) -> None:
        if level and (current_level := int(level)) != self.previous_level:
            self.previous_level = current_level
        if skill and skill != self.previous_skill:
            self.previous_skill = skill
        if mod_id and mod_id != self.previous_mod_id:
            self.previous_mod_id = mod_id

        self.active_manager.add_object(self.previous_mod_id, item_id, self.previous_skill, self.previous_level)
