import json
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import requests
from fastapi import HTTPException
from starlette import status

from api.config.DirectoryInfo import directory_info
from api.router import router
from .config.config import config
from .config.test_users_data import test_data
from .hr_plug import Employee
from .response_schemas.Tours import Tour
from .utils import create_readable_text, get_the_earliest_tour, get_the_cheapest_tour, get_the_earliest_cheapest_tour, \
    count_losses, calc_new_date
from .utils import get_dict_by_key

# from api.utils import get_token
# test_employee = Employee(1, "test", 2, "10.03.2020", 10000, 10000)
test_employees = [Employee(**params) for params in test_data]


@router.get('/tour/',
            status_code=status.HTTP_200_OK,
            response_model=List[Tour],
            summary='Получение списка туров')
def get_tours(user_id: str,
              country: str,  # ид страны назначения. (из чекбокса выбираем)
              city: str,  # ид города вылета (из чекбокса выбираем)
              start_date: str,
              amount_of_days: int,  # кол-во дней отпуска
              price_min: int,
              price_max: int,
              hotel_star: int | None = None
              ):
    if amount_of_days >= 20:
        raise HTTPException(status_code=522, detail=f"Количество дней не может превышать 19")

    try:
        country_id = get_dict_by_key(directory_info.COUNTRIES_DICT, 'name', country)['countryId']
    except TypeError as e:
        raise HTTPException(status_code=404, detail=f"Туры в {country} отсутствуют")

    try:
        city_id = get_dict_by_key(directory_info.CITIES_DICT, 'name', city)['cityId']
    except TypeError as e:
        raise HTTPException(status_code=404, detail=f"Туры из {city} отсутствуют")

    hotelClassBetter = False

    if test_employees is not None:
        employee = next((obj for obj in test_employees if obj.id == user_id), None)  # тестовые данные
    else:
        pass  # получение данных о человеке (зп и кол-во накопленных дней отпуска) из отдела кадров. Заглушка вместо апи согласно тз

    if employee == None:
        raise HTTPException(status_code=404, detail=f'Сотрудник с id {user_id} не найден')

    if hotel_star is None:
        hotel_star = get_dict_by_key(directory_info.HOTEL_CLASS_DICT, 'name', '1 *')['classId']
        hotelClassBetter = True

    start_date = datetime.strptime(start_date, "%d.%m.%Y").date()
    end_date = (start_date + timedelta(
        days=config.TIME_DELTA_FOR_TOUR_SEARCH)).strftime("%d.%m.%Y")

    def create_request_link(start_date, end_date, city_id, country_id, amount_of_days, price_min, price_max,
                            hotelClassBetter):
        return (
            f'https://search.tez-tour.com/tariffsearch/getResult?accommodationId=2&after={start_date.strftime("%d.%m.%Y")}&before={end_date}&cityId={city_id}&countryId={country_id}&nightsMin={amount_of_days}&nightsMax={amount_of_days}&'
            f'currency=5561&priceMin={price_min}&priceMax={price_max}&hotelClassId=2569&hotelClassBetter={hotelClassBetter}&rAndBId=2424&rAndBBetter=true')

    def get_tours_list():
        tour_list_answer = requests.get(
            create_request_link(start_date, end_date, city_id, country_id, amount_of_days, price_min, price_max,
                                hotelClassBetter))
        if tour_list_answer.status_code != 200:
            raise HTTPException(status_code=404, detail=f"API турагентства отправило недействительный ответ")

        try:
            tour_list = create_readable_text(json.loads(tour_list_answer.text))
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Туры по указанным параметрам не найдены")
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Туры по указанным параметрам не найдены")

        losses = count_losses(employee, tour_list)

        tours_df = pd.DataFrame(tour_list)
        try:
            tours_df['Цена с убытком'] = tours_df['Цена'] + losses
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Туры по указанным параметрам не найдены")
        tours_df["Дата заезда"] = pd.to_datetime(tours_df["Дата заезда"], format="%d.%m.%Y")

        return tours_df

    early_tours_df = get_tours_list()
    earliest_tour = get_the_earliest_tour(early_tours_df, 'Самый ранний тур')
    earliest_cheapest_tour = get_the_earliest_cheapest_tour(early_tours_df, 'Самый ранний и дешевый тур')

    if employee.vacationDaysAvailable < amount_of_days:
        date_with_required_vac_days = calc_new_date(employee.vacationDaysAvailable, amount_of_days)
        if start_date < date_with_required_vac_days:
            start_date = date_with_required_vac_days

    end_date = (start_date + timedelta(
        days=config.TIME_DELTA_FOR_TOUR_SEARCH)).strftime(
        "%d.%m.%Y")

    response_data = [earliest_tour, earliest_cheapest_tour]
    try:
        late_tours_df = get_tours_list()
        earliest_tour_without_ad_days = get_the_earliest_cheapest_tour(late_tours_df,
                                                                       'Самый ранний тур без взятия дополнительных дней отпуска за свой счет')
        tours_df = pd.concat([early_tours_df, late_tours_df], ignore_index=True).drop_duplicates()
        response_data.append(earliest_tour_without_ad_days)
    except Exception as e:
        tours_df = early_tours_df

    cheapest_tour = get_the_cheapest_tour(tours_df)
    response_data.append(cheapest_tour)

    response = [
        Tour(date_in=obj['Дата заезда'], amount_of_nights=obj['Длительность в ночах'], area=obj['Регион проживания'],
             hotel=obj['Отель'], room_type=obj['Тип номера'], pansion=obj['Пансион'], price=obj['Цена'],
             availible_rooms=obj['Доступные места в отеле'],
             price_with_loss=obj['Цена с убытком'], category=obj['Категория']) for obj in response_data]

    return response
