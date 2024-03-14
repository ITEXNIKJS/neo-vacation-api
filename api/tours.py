import json
import pandas as pd
from datetime import datetime, timedelta

import requests
from starlette import status

from .config.config import config
from .utils import create_readable_text, get_the_earliest_tour, get_the_cheapest_tour, get_the_earliest_cheapest_tour

from api.config.DirectoryInfo import directory_info
from api.router import router
from .utils import get_dict_by_key


# from api.utils import get_token


@router.get('/tour/',
            status_code=status.HTTP_200_OK,
            #            response_model=List[Tours],
            summary='Получение списка туров')
def get_tours(country: str,  # ид страны назначения. (из чекбокса выбираем)
              city: str,  # ид города вылета (из чекбокса выбираем)
              start_date: str,
              amount_of_days: int, # кол-во дней отпуска
              price_min: int,
              price_max: int,
              hotel_star: int | None = None
              ):
    country_id = get_dict_by_key(directory_info.COUNTRIES_DICT, 'name', country)['countryId']
    city_id = get_dict_by_key(directory_info.CITIES_DICT, 'name', city)['cityId']

    hotelClassBetter = False

    if hotel_star is None:
        hotel_star = get_dict_by_key(directory_info.HOTEL_CLASS_DICT, 'name', '1 *')['classId']
        hotelClassBetter = True

    end_date = (datetime.strptime(start_date, "%d.%m.%Y").date() + timedelta(days=config.TIME_DELTA_FOR_TOUR_SEARCH)).strftime("%d.%m.%Y")

    def create_request_link():
        return (
            f'https://search.tez-tour.com/tariffsearch/getResult?accommodationId=2&after={start_date}&before={end_date}&cityId={city_id}&countryId={country_id}&nightsMin={amount_of_days}&nightsMax={amount_of_days}&'
            f'currency=5561&priceMin={price_min}&priceMax={price_max}&hotelClassId=2569&hotelClassBetter={hotelClassBetter}&rAndBId=2424&rAndBBetter=true')

    tour_list = requests.get(create_request_link()).text
    tour_list = create_readable_text(json.loads(tour_list))

    # Севина крутая вещь с рассчетом убытков

    tours_df = pd.DataFrame(tour_list)
    tours_df["Дата заезда"] = pd.to_datetime(tours_df["Дата заезда"], format="%d.%m.%Y")

    earliest_tour = get_the_earliest_tour(tours_df)
    earliest_cheapest_tour = get_the_earliest_cheapest_tour(tours_df) # сомннительнаф ф-ция в плане логики
    cheapest_tour = get_the_cheapest_tour(tours_df)

    earliest_tour_without_ad_days = get_the_earliest_vacation_without_ad_dates(tours_df, vacation_paid_days)

    return earliest_tour, earliest_cheapest_tour, cheapest_tour, earliest_tour_without_ad_days
