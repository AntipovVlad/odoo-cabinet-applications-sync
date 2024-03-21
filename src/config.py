from yaml import load_all, FullLoader


SYSTEM_PARAMS: dict = {}
PROJECT_NUMBERS: list = []
CABINET_BASE_URL: str = ''


def init_config_settings() -> None:
    global SYSTEM_PARAMS, PROJECT_NUMBERS, CABINET_BASE_URL

    with open('example_config.yaml', encoding='utf-8') as file:
        all_data = list(load_all(file, Loader=FullLoader))[0]

    SYSTEM_PARAMS = all_data['odoo_params']
    CABINET_BASE_URL = all_data['cabinet_base_url']
    PROJECT_NUMBERS = all_data['project_numbers']
