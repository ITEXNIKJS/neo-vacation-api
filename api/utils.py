import math
from datetime import datetime

import pandas as pd
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
        result["Цена"] = float(item[10]['total'])
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


def get_pairs_data_price(df):
    date_in_series = pd.Series(df["date_in"])
    price_series = pd.Series(df["price"])
    pairs = list(zip(date_in_series, price_series))
    return pairs


def get_pairs_data_price_loss(df):
    date_in_series = pd.Series(df["date_in"])
    price_series = pd.Series(df["price_with_loss"])
    pairs = list(zip(date_in_series, price_series))
    return pairs


def get_pairs_area_price(df):
    date_in_series = pd.Series(df["area"])
    price_series = pd.Series(df["price"])
    pairs = list(zip(date_in_series, price_series))
    return pairs


def get_pairs_area_price_loss(df):
    date_in_series = pd.Series(df["area"])
    price_series = pd.Series(df["price_with_loss"])
    pairs = list(zip(date_in_series, price_series))
    return pairs

if __name__ == "__main__":
    data = [
        {
            "date_in": "2024-03-12",
            "amount_of_nights": 3,
            "area": "Расссиииияяяя",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 100.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-09",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 200.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 200.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 200.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 200.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 200.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 200.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-13",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 350.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-18",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 400.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-19",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 150.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-30",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 2000.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-20",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 210.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-21",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 240.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
        {
            "date_in": "2024-03-22",
            "amount_of_nights": 3,
            "area": "Москва",
            "hotel": "Примерный",
            "room_type": "Стандартный",
            "price": 230.0,
            "availible_rooms": "Да",
            "price_with_loss": 90.0,
            "category": "Эконом",
            "buy_date": "2024-03-05",
        },
    ]


    def get_df(data):
        for entry in data:
            entry["date_in"] = pd.to_datetime(entry["date_in"])
            entry["buy_date"] = pd.to_datetime(entry["buy_date"])

        return pd.DataFrame(data)

    df = get_df(data)
    print(get_pairs_area_price_loss(df))



