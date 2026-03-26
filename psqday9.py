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


class car:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price
        
    def show(self):
        print("Brand :", self.brand )
        print("Price :", self.price)
        
        
c1 = car("BMW", 50000000)
c1.show()

print("--------------------------")

c2 = car("Audi", 60000000)
c2.show()