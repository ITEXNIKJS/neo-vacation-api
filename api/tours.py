import json
from datetime import datetime

import requests
from starlette import status
from utils import create_readable_text

from api.config.DirectoryInfo import directory_info
from api.router import router
from api.utils import get_dict_by_key


# from api.utils import get_token


@router.get('/tour/',
            status_code=status.HTTP_200_OK,
            #            response_model=List[Tours],
            summary='Получение списка туров')
def get_tours(country: str,  # ид страны назначения. (из чекбокса выбираем)
              city: str,  # ид города вылета (из чекбокса выбираем)
              start_date: str,
              end_date: str,
              price_min: int,
              price_max: int,
              hotel_star: int | None = None
              #              token: str = Depends(get_token)
              ):
    # всунуть эту проверку на даты, которую требует апи
    country_id = get_dict_by_key(directory_info.COUNTRIES_DICT, 'name', country)['countryId']
    city_id = get_dict_by_key(directory_info.CITIES_DICT, 'name', city)['cityId']

    def get_amount_of_nights(date1, date2):
        date1 = datetime.strptime(date1, "%d.%m.%Y").date()
        date2 = datetime.strptime(date2, "%d.%m.%Y").date()
        delta = date2 - date1
        amount_of_nights = delta.days
        return amount_of_nights

    amount_of_nights = get_amount_of_nights(start_date, end_date)

    hotelClassBetter = False

    if hotel_star is None:
        hotel_star = get_dict_by_key(directory_info.HOTEL_CLASS_DICT, 'name', '1 *')['classId']
        hotelClassBetter = True

    # ТЕСТОВОЕ ЗНАЧЕНИЕ!!
    rAndBId = 2424
    rAndBBetter = True

    def create_request_link():
        return (
            f'https://search.tez-tour.com/tariffsearch/getResult?accommodationId=2&after={start_date}&before={end_date}&cityId={city_id}&countryId={country_id}&nightsMin={amount_of_nights}&nightsMax={amount_of_nights}&'
            f'currency=5561&priceMin={price_min}&priceMax={price_max}&hotelClassId=2569&hotelClassBetter={hotelClassBetter}&rAndBId=2424&rAndBBetter=true')

    tour_list = requests.get(create_request_link()).text
    
    return create_readable_text(json.loads(tour_list))
