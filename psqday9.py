
# # Q1: Create a class Mobile:*********************************************************************
# # brand******************************************************************************************
# # price*****************************************************************************************
# # function show()*********************************************************************************

# class Mobile:
#     def __init__(self, brand, price):
#         self.brand = brand
#         self.price = price
    
#     def show(self):
#         print("Brand :", self.brand)
#         print("Price :", self.price)

# # Object banao
# m1 = Mobile("Samsung", 15000)
# m1.show()

# print("-------------------")

# m2 = Mobile("iPhone", 80000)
# m2.show()

# # Q2: Create 2 objects:*************************************************************************
# # BMW***************************************************************************************
# # Audi***************************************************************************************

# class car:
#     def __init__(self, brand, price):
#         self.brand = brand
#         self.price = price
        
#     def show(self):
#         print("Brand :", self.brand )
#         print("Price :", self.price)
        
# # object 1 - BMW
# c1 = car("BMW", 50000000)

# # object 2 - Audi
# c2 = car("Audi", 60000000)

# print("=====Car - 1 =====")
# c1.show()

# print("====Car - 2 ======")
# c2.show()


# class person:
#     # name = "Mohit"
#     # occ = "Developer"
    
#     def __init__(self, name, occ):
#         self.name = name
#         self.occ = occ
    
#     def info(self):
#         print(f"{self.name} is a {self.occ}")
        
#         # print(self.name)
#         # print(self.occ)
   
# a = person("Mohit", "Developer")
# b = person("Sulekha", "Doctor")
# a.info()
# b.info()


# class Employee:
#     def __init__(self, name, id):
#         self.name = name
#         self.id = id
        
#     def showDetails(self):
#         print(f"The name of Employee: {self.id} is {self.name}")

# class Programmer(Employee):                     # Single Inheritance(parent one and child one) 
    
#     def __init__(self, name, id):
#         self.id = id
#         self.name = name
    
#     def showLangauge(self):
#         print(f"The default langauge is python. id is {self.id} and name {self.name}")
        
# class Subject(Programmer):                      # Hierarchical Inheritance(one parent multiple child)
#     def __init__(self, name, id):
#         self.id = id
#         self.name = name
        
#     def showSubject(self):
#         print(f"Python subject is a good subject for id is {self.id} name {self.name}")        
        
# e1 = Employee("Mohit kumar", 1530)
# e1.showDetails()
# e2 = Programmer("Munna kumar", 1508)
# e2.showLangauge()
# e3 = Subject("Mohit kumar", 3015)
# e3.showSubject()


# class Math:                                       # Staticmethod
#     def __init__(self, num):
#         self.num = num
        
#     def addtonum(self, n):
#         self.num = self.num + n
        
#     @staticmethod
#     def add(a, b):
#         return a + b
    
# a = Math(5)
# print(a.num)
# a.addtonum(6)
# print(a.num)


# # class methoda alternative

# class Employee:
#     def __init__(self, name, salary):
#         self.name = name
#         self.salary = salary
        
#     @classmethod
#     def fromStr(cls, string):
#         return cls(string.split("-")[0], string.split("-")[1])
    
# e1 = Employee("Mohit", 30000)
# print(e1.name)
# print(e1.salary)

# string = "Munna-32000"
# e2 = Employee.fromStr(string)
# print(e2.name)
# print(e2.salary)


# class shape:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
        
#     def area(self):
#         return self.x * self.y
    
# class Circle:
#     def __init__(self, radius):
#         self.radius = radius
        
#     def area(self):
#         return 3.14 * self.radius *self.radius
    
# rec = Circle(5)  
# print(rec.area())
    
# rec = shape(3, 4)
# print(rec.area())

class Bank:
    def __init__(self, balance):
        self.__balance = balance    # private variable

    # Deposit money
    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount!")
        else:
            self.__balance += amount
            print("Deposited: ₹", amount)

    # Withdraw money
    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount!")
        elif amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount
            print("Withdrawn: ₹", amount)

    # Show balance
    def show_balance(self):
        print("Current Balance: ₹", self.__balance)


# Object 
acc = Bank(10000)

while True:
    print("\n===== BANK MENU =====")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    # Option 1 - Show Balance
    if choice == 1:
        acc.show_balance()

    # Option 2 - Deposit
    elif choice == 2:
        amount = int(input("Enter deposit amount: ₹"))
        acc.deposit(amount)

    # Option 3 - Withdraw
    elif choice == 3:
        amount = int(input("Enter withdraw amount: ₹"))
        acc.withdraw(amount)

    # Option 4 - Exit
    elif choice == 4:
        print("\n==============================")
        print("👋 Goodbye! See you again!")
        print("==============================")
        exit()

    else:
        print("Invalid choice! Please select 1-4")
