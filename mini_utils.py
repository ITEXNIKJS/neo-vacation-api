import math
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta


def get_value_USD():
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    return data["Valute"]["USD"]["Value"]


# def calc_new_date(current_vacation_days, required_vacation_days):
#     today = datetime.today()

#     if required_vacation_days > current_vacation_days:
#         count = 0
#         while required_vacation_days > current_vacation_days:
#             current_vacation_days += 28
#             count += 1
#         return datetime(today.year + count, 1, 1).date()
#     else:
#         return today.strftime("%Y-%m-%d")


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


if __name__ == "__main__":
    current_vacation_days = 9
    required_vacation_days = 8

    print(calc_new_date(current_vacation_days, required_vacation_days))
