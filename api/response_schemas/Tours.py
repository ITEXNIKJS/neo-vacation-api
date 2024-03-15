from pydantic import BaseModel, Field


class Tour(BaseModel):
    date_in: str = Field(..., serialization_alias='Дата заезда')
    city: str = Field(..., serialization_alias='Город вылета')
    amount_of_nights: int = Field(..., serialization_alias='Длительность в ночах')
    area: str = Field(..., serialization_alias='Регион проживания')
    hotel: str = Field(..., serialization_alias='Отель')
    pansion: str = Field(..., serialization_alias='Пансион')
    room_type: str = Field(..., serialization_alias='Тип номера')
    price: float = Field(..., serialization_alias='Цена')
    availible_rooms: str = Field(..., serialization_alias='Доступные места в отеле')
    price_with_loss: float = Field(..., serialization_alias='Цена с убытком')
    category: str = Field(..., serialization_alias='Категория')
