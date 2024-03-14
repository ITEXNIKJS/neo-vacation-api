from hr_plug import *

def count_losses(employee, tours):
    if not tours:
        return -1
    if type(tours) is list:
        for tour in tours:
            payment, losses = employee.vacation_pay(list(tour["Длительность в ночах"])[0])
            tour["Цена"] -= losses
    else:
        payment, losses = employee.vacation_pay(list(tours["Длительность в ночах"])[0])
        tours["Цена"] -= losses
    return tours

#test = [{'Дата заезда': {'19.03.2024'}, 'Длительность в ночах': {10}, 'Регион проживания': {'Белек'}, 'Отель': {'PRENSES SEALINE BEACH HOTEL 4 *'}, 'Пансион': {'Только завтраки'}, 'Тип номера': {'Economy Room without Balcony'}, 'Цена': 102922.11, 'Доступные места в отеле': [['https://online.tez-tour.com/armmanager/workplace/section/new-order?depCity=345&arrivalCity=345&hotStType=2&locale=ru&priceOfferId=21969333&cResId=277490456155&cFlyIds=227480733&ftt=3635&ltt=3635&ftv=&ltv=&sk=1&promo=1&rar=487545&rdr=487545', '']]}]
#employee = Employee(1, "test", 2, "10.03.2020", 10000, 10000)
#print(count_losses(employee, test))

