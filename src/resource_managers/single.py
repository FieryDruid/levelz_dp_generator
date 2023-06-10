import json

from src.enums import UnlockTypes, AvailableSkills
from src.resource_managers.base import ResourceManager


class SingleUnlockManager(ResourceManager):
    unlock_type: UnlockTypes

    @property
    def unlock_type(self) -> UnlockTypes:
        raise NotImplementedError

    @property
    def base_dict(self) -> dict[str, any]:
        return {
            'replace': False,
            'skill': '',
            'level': 0,
            self.unlock_type.name: f'minecraft:custom_{self.unlock_type.name}',
        }

    def add_object(self, mod_id: str, object_id: str, skill: AvailableSkills, level: int = 0):
        current_info = self.base_dict
        current_info['skill'] = skill.name
        object_string = ':'.join([mod_id, object_id])
        current_info['object'] = object_string
        current_info['level'] = level
        mod_path = self.base_path / mod_id
        mod_path.mkdir(exist_ok=True, parents=True)
        item_path = mod_path / f'{object_id}_unlock.json'
        with item_path.open('w') as json_file:
            json.dump(current_info, json_file, indent=4)
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        print(f'Item <{current_info["object"]}> successfully added into <{skill.name}> unlock!')
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')


class BlockUnlockManager(SingleUnlockManager):
    unlock_type = UnlockTypes.block


class ItemUnlockManager(SingleUnlockManager):
    unlock_type = UnlockTypes.item


class EntityUnlockManager(SingleUnlockManager):
    unlock_type = UnlockTypes.entity
