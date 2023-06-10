from src.constructor import DatapackConstructor
from src.enums import SupportedTypes
from src.resource_managers.base import get_types_info

VERSIONS_MATCH = {
    '1.19.4': 12,
    '1.19.3': 10,
    '1.19.2': 10,
    '1.19.1': 10,
    '1.19': 10,
    '1.18.2': 9,
    '1.18.1': 8,
    '1.18': 8,
}


def get_versions_info() -> str:
    return '\n'.join([version for version in VERSIONS_MATCH])


def get_pack_format_by_version(version: str) -> int:
    return VERSIONS_MATCH.get(version, 10)


if __name__ == '__main__':
    pack_format = get_pack_format_by_version(
        input(
            '\n'.join(['Gen datapack for version:', get_versions_info(), '> '])
        )
    )
    pack_name = input('Datapack name (leave blank for default: <MoreLevelZ>):\n> ')
    description = input('Datapack description (may be empty):\n> ')
    constructor = DatapackConstructor(pack_format, pack_name, description)
    current_type = None
    while True:
        object_pieces = [f'Datapack object type:\n\t{get_types_info()}']
        if current_type:
            object_pieces.append(f'\n\t-> Previous type: <{current_type.name}>\n\tLeave blank for previous value')
        object_msg = ''.join(object_pieces)
        object_type = input(f'{object_msg}\n> ')
        if object_type:
            current_type = SupportedTypes.get_by(object_type)
        constructor.make_for = current_type
        input_data = constructor.input()
        constructor.add(input_data.mod_id, input_data.object_id, input_data.skill, input_data.level)
