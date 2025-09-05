class Employee:
    def __init__ (self, name, salary):
        self.name = name
        self.salary = salary
    def promotion(self):
        return (self.salary*1.10)

John = Employee("John", 5000)

print ("Updated salary: ", John.promotion())
