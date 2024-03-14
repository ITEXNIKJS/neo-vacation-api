import json

from fastapi.security import HTTPBearer

security = HTTPBearer(scheme_name='Authorization')


def get_dict_by_key(list_of_dicts, key_name, key_value):
    """Получение словаря из списка словарей, у которого есть одно из полей равно заданному значению"""
    return next((dict for dict in list_of_dicts if dict[key_name] == key_value), None)


def create_readable_text(json_file_path):
    """Полученный json от API перемалывает в читабельный вид"""
    """Пример использования result = create_readable_text("temp.json")"""

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    result_string = ""

    for item in data['data']:
        result_string += f"Дата заезда: {item[0]}, \n"
        result_string += f"Регион проживания: {item[5][0]}, \n"
        result_string += f"Отель: {item[6][1]}, \n"
        result_string += f"Пансион: {item[7][1]}, \n"
        result_string += f"Тип номера: {item[8][1]}, \n"
        result_string += f"Цена: {item[10]['currency']} {item[10]['total']}, \n"
        result_string += f"Доступные места в отеле: {item[11]}, \n"
        result_string += "\n"

    return result_string
