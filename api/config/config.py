class ToursConfig:
    DIRECTORY_URL = 'https://search.tez-tour.com/tariffsearch/references?locale=ru&formatResult=true&xml=false'
    CURRENCIES_KEY_NAME = 'currencies'
    CURRENCY_NAME = 'Рубль'
    COUNTRIES_KEY_NAME = 'countries'
    CITIES_KEY_NAME = 'cities'
    HOTEL_CLASS_KEY_NAME = 'hotelClasses'
    TIME_DELTA_FOR_TOUR_SEARCH = 20 # указывается в днях

config = ToursConfig()
