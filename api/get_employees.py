import json
from hr_plug import *

#Получить сотрудника из БД по его идентификатору
def get_employee_by_id(employee_id, filename="hr.json"):
    with open(filename, "r") as file:
        data = json.load(file)
        for employee_data in data:
            if employee_data['id'] == employee_id:
                employee = Employee(employee_data["id"],
                                    employee_data["name"],
                                    employee_data["vacationDaysAvailable"],
                                    employee_data["lastVacation"],
                                    employee_data["currentSalary"],
                                    employee_data["avgSalary"], )
                return employee
    return None
