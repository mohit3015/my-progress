
# Q1: Create a class Mobile:*********************************************************************
# brand******************************************************************************************
# price*****************************************************************************************
# function show()*********************************************************************************

class Mobile:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price
    
    def show(self):
        print("Brand :", self.brand)
        print("Price :", self.price)

# Object banao
m1 = Mobile("Samsung", 15000)
m1.show()

print("-------------------")

m2 = Mobile("iPhone", 80000)
m2.show()

# Q2: Create 2 objects:*************************************************************************
# BMW***************************************************************************************
# Audi***************************************************************************************

class car:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price
        
    def show(self):
        print("Brand :", self.brand )
        print("Price :", self.price)
        
# object 1 - BMW
c1 = car("BMW", 50000000)

# object 2 - Audi
c2 = car("Audi", 60000000)

print("=====Car - 1 =====")
c1.show()

print("====Car - 2 ======")
c2.show()


class person:
    # name = "Mohit"
    # occ = "Developer"
    
    def __init__(self, name, occ):
        self.name = name
        self.occ = occ
    
    def info(self):
        print(f"{self.name} is a {self.occ}")
        
        # print(self.name)
        # print(self.occ)
   
a = person("Mohit", "Developer")
b = person("Sulekha", "Doctor")
a.info()
b.info()


class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def showDetails(self):
        print(f"The name of Employee: {self.id} is {self.name}")

class Programmer(Employee):
    
    def __init__(self, name, id):
        self.id = id
        self.name = name
    
    def showLangauge(self):
        print(f"The default langauge is python. id is {self.id} and name {self.name}")
        
class Subject(Programmer):
    def __init__(self, name, id):
        self.id = id
        self.name = name
        
    def showSubject(self):
        print(f"Python subject is a good subject for id is {self.id} name {self.name}")        
        
e1 = Employee("Mohit kumar", 1530)
e1.showDetails()
e2 = Programmer("Munna kumar", 1508)
e2.showLangauge()
e3 = Subject("Mohit kumar", 3015)
e3.showSubject()