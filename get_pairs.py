import pandas as pd
import plotly.express as px

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
    df = get_df(data)
    print(get_pairs_area_price_loss(df))
