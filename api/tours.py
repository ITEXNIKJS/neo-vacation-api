import json
from datetime import datetime, timedelta

import pandas as pd
import requests
from starlette import status

from api.config.DirectoryInfo import directory_info
from api.router import router
from .config.config import config
from .config.test_users_data import test_data
from .hr_plug import Employee
from .utils import create_readable_text, get_the_earliest_tour, get_the_cheapest_tour, get_the_earliest_cheapest_tour, \
    count_losses
from .utils import get_dict_by_key

# from api.utils import get_token
# test_employee = Employee(1, "test", 2, "10.03.2020", 10000, 10000)
test_employees = [Employee(**params) for params in test_data]


@router.get('/tour/',
            status_code=status.HTTP_200_OK,
            #            response_model=List[Tours],
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
    try:
        country_id = get_dict_by_key(directory_info.COUNTRIES_DICT, 'name', country)['countryId']
        city_id = get_dict_by_key(directory_info.CITIES_DICT, 'name', city)['cityId']
    except TypeError as e:
        raise TypeError(f'Указанный страна/город не существуют. {e}')

    hotelClassBetter = False

    if test_employees is not None:
        employee = next((obj for obj in test_employees if obj.id == user_id), None)  # тестовые данные
    else:
        pass  # получение данных о человеке (зп и кол-во накопленных дней отпуска) из отдела кадров. Заглушка вместо апи согласно тз

    if employee == None:
        raise ValueError(f'Сотрудник с id {user_id} не найден')

    if hotel_star is None:
        hotel_star = get_dict_by_key(directory_info.HOTEL_CLASS_DICT, 'name', '1 *')['classId']
        hotelClassBetter = True

    end_date = (datetime.strptime(start_date, "%d.%m.%Y").date() + timedelta(
        days=config.TIME_DELTA_FOR_TOUR_SEARCH)).strftime("%d.%m.%Y")

    def create_request_link(start_date, end_date, city_id, country_id, amount_of_days, price_min, price_max,
                            hotelClassBetter):
        return (
            f'https://search.tez-tour.com/tariffsearch/getResult?accommodationId=2&after={start_date}&before={end_date}&cityId={city_id}&countryId={country_id}&nightsMin={amount_of_days}&nightsMax={amount_of_days}&'
            f'currency=5561&priceMin={price_min}&priceMax={price_max}&hotelClassId=2569&hotelClassBetter={hotelClassBetter}&rAndBId=2424&rAndBBetter=true')

    def get_tours_list():
        tour_list = requests.get(
            create_request_link(start_date, end_date, city_id, country_id, amount_of_days, price_min, price_max,
                                hotelClassBetter)).text
        tour_list = create_readable_text(json.loads(tour_list))

        losses = count_losses(employee, tour_list)

        tours_df = pd.DataFrame(tour_list)
        tours_df['Цена с убытком'] = tours_df['Цена'] + losses
        tours_df["Дата заезда"] = pd.to_datetime(tours_df["Дата заезда"], format="%d.%m.%Y")

        return tours_df

    early_tours_df = get_tours_list()
    earliest_tour = get_the_earliest_tour(early_tours_df, 'Самый ранний тур')
    earliest_cheapest_tour = get_the_earliest_cheapest_tour(early_tours_df, 'Самый ранний и дешевый тур')

    # if employee.vacationDaysAvailable < amount_of_days:
    #     # start_date = start_date + timedelta(
    #     #     days=calc_new_date(employee.vacationDaysAvailable, amount_of_days)).strftime(
    #     #     "%d.%m.%Y")
    start_date = start_date
    end_date = (datetime.strptime(start_date, "%d.%m.%Y").date() + timedelta(
        days=config.TIME_DELTA_FOR_TOUR_SEARCH)).strftime(
        "%d.%m.%Y")

    late_tours_df = get_tours_list()
    earliest_tour_without_ad_days = get_the_earliest_cheapest_tour(late_tours_df,
                                                                   'Самый ранний тур без взятия дополнительных дней отпуска за свой счет')

    tours_df = pd.concat([early_tours_df, late_tours_df], ignore_index=True).drop_duplicates()
    cheapest_tour = get_the_cheapest_tour(tours_df)

    response = [earliest_tour, cheapest_tour, earliest_cheapest_tour, earliest_tour_without_ad_days]

    return response
