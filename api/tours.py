from datetime import datetime
from typing import List

from starlette import status

from api.config.DirectoryInfo import directory_info
from api.config.config import config
from api.router import router
from fastapi import Depends

from api.utils import get_dict_by_key


#from api.utils import get_token


@router.get('/buildings/',
            status_code=status.HTTP_200_OK,
            tags=['buildings'],
#            response_model=List[Tours],
            summary='Получение информации о здании по фрагменту адреса')
def get_tours(country: str, # ид страны назначения. (из чекбокса выбираем)
              city: str, # ид города вылета (из чекбокса выбираем)
              start_date: str,
              end_date: str,
              price_min: float,
              price_max: float,
              hotel_star: int | None = None
#              token: str = Depends(get_token)
              ):
    # всунуть эту проверку на даты, которую требует апи
    country_id = get_dict_by_key(directory_info.COUNTRIES_DICT, 'name', country)['countryId']
    city_id = get_dict_by_key(directory_info.CITIES_DICT, 'name', city)['countryId']

    def get_amount_of_nights(date1, date2):
        date1 = datetime.strptime(date1, "%Y.%m.%d").date()
        date2 = datetime.strptime(date2, "%Y.%m.%d").date()
        delta = date2 - date1
        amount_of_nights = delta.days
        return amount_of_nights

    amount_of_nights = get_amount_of_nights(start_date, end_date)
    accomodation = 2

    return country_id, city_id
    # get_list_of_tours()
    # filter_tours()
    # return list_of_tours
