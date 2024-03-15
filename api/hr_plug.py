from datetime import datetime, timedelta

split_char = '|'
days_in_month = 29.3 # Среднее кол-во дней в месяце, даёт лишь примерный результат


Holidays = [
    "01.01.2024",    "02.01.2024",
    "03.01.2024",    "04.01.2024",
    "05.01.2024",    "06.01.2024",
    "08.01.2024",    "07.01.2024",
    "23.02.2024",    "08.03.2024",
    "01.05.2024",
    "09.05.2024",    "12.06.2024",
    "04.11.2024"
]


class Employee:
    id = -1
    name = "Test Data"
    vacationDaysAvailable = 0
    lastVacation = "01.01.2024"
    currentSalary = 10000
    avgSalary = 10000 #Средняя зарплата за месяц за последний год

    def __init__(self, id, name, vacationDaysAvailable, lastVacation, currentSalary, avgSalary):
        self.id = id
        self.name = name
        self.vacationDaysAvailable = vacationDaysAvailable
        self.lastVacation = lastVacation
        self.currentSalary = currentSalary
        self.avgSalary = avgSalary

    #Расчитать отпускные и дополнительные убытки сотрудника, если отпускных мало
    def vacation_pay(self, departureDay, tourDurationInDays):
        #TODO: учёт праздничных дней!!!
        #среднегодовой заработок * кол-во дней в отпуске / среднее кол-во дней в месяце
        coef = tourDurationInDays #сколько дней оплачивается
        employeeLosses = 0 #Убытки сотрудника, если ему не хватило дней
        totalPaidDays = self.count_available_days(departureDay, tourDurationInDays)

        #если дней отпуска не хватило
        if (totalPaidDays < tourDurationInDays):
            coef = tourDurationInDays - totalPaidDays
            employeeLosses = self.avgSalary / days_in_month * (tourDurationInDays - totalPaidDays)
            employeeLosses += self.avgSalary / days_in_month * (totalPaidDays - coef)

        vacationPay = self.avgSalary / days_in_month * coef
        return vacationPay, employeeLosses

    #Расчитать, сколько дней отпуска будет накоплено к дате отправления в тур
    def count_available_days(self, departureDate, tourDurationInDays):
        startDate = datetime.strptime(self.lastVacation, "%d.%m.%Y").date()
        endDate = datetime.strptime(departureDate, "%d.%m.%Y").date()
        totalPaidDays = self.vacationDaysAvailable

        #Прибавление новых отпускных, если прошёл год
        if (endDate - startDate >= timedelta(365)):
            totalPaidDays += 28

        #Смотрим, будут ли праздники во время тура
        checkDate = endDate
        for i in range(tourDurationInDays):
            date_str = checkDate.strftime("%d.%m.%Y")
            if (date_str in Holidays):
                totalPaidDays += 1
            checkDate += timedelta(days=1)
        print("totalPaidDays: ", totalPaidDays)
        return totalPaidDays
