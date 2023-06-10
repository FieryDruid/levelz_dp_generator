import json

from src.enums import UnlockTypes, AvailableSkills
from src.resource_managers.base import ResourceManager
from src.support import InputData


class MultipleUnlockManager(ResourceManager):
    unlock_type: UnlockTypes

    @property
    def base_dict(self) -> dict[str, any]:
        return {
            'replace': False,
            'level': '',
            self.unlock_type.name: [],
        }

    def user_input(self, previous_mod_id: str | None, _: AvailableSkills, previous_level: int | None) -> InputData:
        if previous_mod_id is None:
            mod_id = None
            while not mod_id:
                mod_id = input('Mod id\n> ')
        else:
            mod_id = input(
                f'Mod id\n\t-> Previous mod_id: <{previous_mod_id}>\n\tLeave blank for use previous value\n> ')

        item_id = input('Item ID:\n> ')

        if previous_level is None:
            level = None
            while not level:
                level = input(f'Item level:\n> ')
        else:
            level = input(f'Item level:\n\t-> Previous: <{previous_level}>\n\tLeave blank for previous value\n> ')
        return InputData(mod_id or previous_mod_id, item_id, None, level or previous_level)

    def add_object(self, mod_id: str, object_id: str, _: any, level: int | None = None):
        self.base_path.mkdir(exist_ok=True, parents=True)
        current_level = level or 0
        level_file = self.base_path / f'level_{current_level}.json'
        if not level_file.exists():
            current_json = self.base_dict
        else:
            with level_file.open('r') as file:
                current_json = json.load(file)

        current_json['level'] = current_level

        new_object_name = f'{mod_id}:{object_id}'
        current_json[self.unlock_type.name].append(new_object_name)

        with level_file.open('w') as new_file:
            json.dump(current_json, new_file, indent=4)
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        print(f'Item <{new_object_name}> successfully added into <{current_level}> level!')
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print()


class ProfessionItemsManager(MultipleUnlockManager):
    objects_list_key = UnlockTypes.item


class ProfessionBlocksManager(MultipleUnlockManager):
    objects_list_key = UnlockTypes.block
