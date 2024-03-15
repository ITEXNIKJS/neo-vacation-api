import math
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta
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
        result["Цена"] = float(item[10]['total']) * get_value_USD()
        result["Доступные места в отеле"] = item[11][0][0]
        result_list.append(result)

    return result_list


def get_the_earliest_tour(tour_df, category_name):
    """сортировка по дате. берется одна из записей, если даты совпадают"""
    min_date = tour_df['Дата заезда'].min()
    filtered_df = tour_df[tour_df['Дата заезда'] == min_date]
    min_date_row = filtered_df.tail(1)
    min_date_dict = min_date_row.to_dict(orient='records')[0]


    min_date_dict['Категория'] = category_name
    min_date_dict['Цена с убытком'] = round(min_date_dict['Цена с убытком'], 2)
    min_date_dict['Цена'] = round(min_date_dict['Цена'], 2)
    min_date_dict['Дата заезда'] = min_date_dict['Дата заезда'].strftime('%d.%m.%Y')
    return min_date_dict


def get_the_cheapest_tour(tour_df):
    """сортировка по цене"""
    cheapest_row = tour_df.loc[tour_df["Цена с убытком"].idxmin()]
    # Преобразование найденной строки в словарь
    cheapest_dict = cheapest_row.to_dict()
    cheapest_dict['Категория'] = 'Самый дешевый тур'
    cheapest_dict['Цена с убытком'] = round(cheapest_dict['Цена с убытком'], 2)
    cheapest_dict['Цена'] = round(cheapest_dict['Цена'], 2)
    cheapest_dict['Дата заезда'] = cheapest_dict['Дата заезда'].strftime('%d.%m.%Y')
    return cheapest_dict


def get_the_earliest_cheapest_tour(tour_df, category_name):
    """сначала сортировка по дате, потом уже по цене"""
    result_dict = tour_df.sort_values(by=["Дата заезда", "Цена с убытком"]).iloc[0].to_dict()
    result_dict['Категория'] = category_name
    result_dict['Цена с убытком'] = round(result_dict['Цена с убытком'], 2)
    result_dict['Цена'] = round(result_dict['Цена'], 2)
    result_dict['Дата заезда'] = result_dict['Дата заезда'].strftime('%d.%m.%Y')
    return result_dict


def count_losses(employee, tours):
    if not tours:
        return -1
    if type(tours) is list:
        tour = tours[0]
    else:
        tour = tours
    payment, losses = employee.vacation_pay(tour["Длительность в ночах"])
    return losses


def get_value_USD():
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    return data["Valute"]["USD"]["Value"]


def calc_new_date(current_vacation_days, required_vacation_days):
    today = datetime.today()
    # в будущем можно передавать в параметры
    base_count_vac_days = 28
    if required_vacation_days > current_vacation_days:
        remaining_days = required_vacation_days - current_vacation_days
        # Если вдруг накопится в течение month то окргуление до след значения
        add_month = math.ceil(remaining_days / (base_count_vac_days / 12))
        vacation_date = today + relativedelta(months=add_month)
        return vacation_date.date()
    else:
        return today.date()


if __name__ == "__main__":
    current_vacation_days = 9
    required_vacation_days = 8

    print(calc_new_date(current_vacation_days, required_vacation_days))

if __name__ == '__main__':
    # test = [{'Дата заезда': '19.03.2024', 'Длительность в ночах': 10, 'Регион проживания': {'Белек'},
    #          'Отель': {'PRENSES SEALINE BEACH HOTEL 4 *'}, 'Пансион': 'Только завтраки',
    #          'Тип номера': {'Economy Room without Balcony'}, 'Цена': 102922.11, 'Доступные места в отеле': [[
    #                                                                                                             'https://online.tez-tour.com/armmanager/workplace/section/new-order?depCity=345&arrivalCity=345&hotStType=2&locale=ru&priceOfferId=21969333&cResId=277490456155&cFlyIds=227480733&ftt=3635&ltt=3635&ftv=&ltv=&sk=1&promo=1&rar=487545&rdr=487545',
    #                                                                                                             '']]}]
    # employee = Employee(1, "test", 2, "10.03.2020", 10000, 10000)
    print(get_value_USD())
