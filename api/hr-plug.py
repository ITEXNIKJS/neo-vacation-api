# Среднее кол-во дней в месяце, даёт лишь примерный результат

split_char = '|'
days_in_month = 29.3
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

    #Расчитать отпускные
    def vacation_pay(self, vacationDays):
        #среднегодовой заработок * кол-во дней в отпуске / среднее кол-во дней в месяце
        coef = vacationDays
        if (self.vacationDaysAvailable < vacationDays):
            coef = vacationDays - self.vacationDaysAvailable
        vacationPay = self.avgSalary * coef / days_in_month
        return vacationPay


