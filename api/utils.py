from fastapi.security import HTTPBearer

security = HTTPBearer(scheme_name='Authorization')


def get_dict_by_key(list_of_dicts, key_name, key_value):
    """Получение словаря из списка словарей, у которого есть одно из полей равно заданному значению"""
    return next((dict for dict in list_of_dicts if dict[key_name] == key_value), None)


def create_readable_text(data):
    """Полученный json от API перемалывает в читабельный вид"""
    """Пример использования result = create_readable_text(data)"""

    result_list = []

    for item in data['data']:
        result = {}
        result["Дата заезда"] = item[0]
        result["Длительность в ночах"] = item[3]
        result["Регион проживания"] = item[5][0]
        result["Отель"] = item[6][1]
        result["Пансион"] = item[7][1]
        result["Тип номера"] = item[8][1]
        result["Цена"] = float(item[10]['total']) * 90
        result["Доступные места в отеле"] = item[11][0][0]
        result_list.append(result)

    return result_list
# print(create_readable_text('test.json'))
