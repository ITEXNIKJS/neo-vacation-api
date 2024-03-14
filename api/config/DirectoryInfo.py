import json

import requests

from api.config.config import config


class DirectoryInfo:
    def __init__(self):
        RUBLES_ID = None
        COUNTRIES_DICT = None
        CITIES_DICT = None
        self.parse_directory()

    def parse_directory(self):
        directory = json.loads(self.download_countries_and_cities_directory())
        self.RUBLES_ID = self.get_dict_by_key(directory[config.CURRENCIES_KEY_NAME], 'name', config.CURRENCY_NAME)
        self.COUNTRIES_DICT = directory[config.COUNTRIES_KEY_NAME]
        self.CITIES_DICT = directory[config.CITIES_KEY_NAME]

    def download_countries_and_cities_directory(self):
        """get all countries and cities"""
        directory_response = requests.get(config.DIRECTORY_URL)
        status_code = directory_response.status_code
        if status_code != 200:
            raise ValueError(f'Произошла ошибка при выгрузке справочника турагентства, {directory_response.text}')

        return directory_response.text

    def get_dict_by_key(self, list_of_dicts, key_name, key_value):
        """Получение словаря из списка словарей, у которого есть одно из полей равно заданному значению"""
        return next((dict for dict in list_of_dicts if dict[key_name] == key_value), None)


directory_info = DirectoryInfo()
if __name__ == '__main__':
    print(directory_info.RUBLES_ID)
    print('countries: ', directory_info.COUNTRIES_DICT)
    print('cities: ', directory_info.CITIES_DICT)
