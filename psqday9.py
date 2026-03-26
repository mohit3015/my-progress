
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