from typing import List

from starlette import status

from api.router import router
from fastapi import Depends

from api.utils import get_token


@router.get('/buildings/',
            status_code=status.HTTP_200_OK,
            tags=['buildings'],
            response_model=List[Tours],
            summary='Получение информации о здании по фрагменту адреса')
def get_tours(country: str, # ид страны назначения. (из чекбокса выбираем)
              city: str, # ид города вылета (из чекбокса выбираем)
                  token: str = Depends(get_token)):
    get_list_of_tours()
    filter_tours()
    return list_of_tours
