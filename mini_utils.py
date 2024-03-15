from datetime import datetime


def calc_new_date(current_vacation_days, required_vacation_days):
    today = datetime.today()

    if required_vacation_days > current_vacation_days:
        count = 0
        while required_vacation_days > current_vacation_days:
            current_vacation_days += 28
            count += 1
        return datetime(today.year + count, 1, 1).date()
    else:
        return today.strftime("%Y-%m-%d")


if __name__ == "__main__":
    current_vacation_days = 5
    required_vacation_days = 8

    print(calc_new_date(current_vacation_days, required_vacation_days))
