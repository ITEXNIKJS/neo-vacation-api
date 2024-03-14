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

    #Расчитать отпускные и дополнительные убытки сотрудника, если отпускных мало
    def vacation_pay(self, vacationDays):
        #среднегодовой заработок * кол-во дней в отпуске / среднее кол-во дней в месяце
        coef = vacationDays #сколько дней оплачивается
        employeeLosses = 0 #Убытки сотрудника, если ему не хватило дней

        #если дней отпуска не хватило
        if (self.vacationDaysAvailable < vacationDays):
            coef = vacationDays - self.vacationDaysAvailable
            employeeLosses = self.avgSalary / days_in_month * (vacationDays - self.vacationDaysAvailable)
            employeeLosses += self.avgSalary / days_in_month * (self.vacationDaysAvailable - coef)

        vacationPay = self.avgSalary / days_in_month * coef
        return vacationPay, employeeLosses


