
# # example from youtube**************************

a = int(input("Enter your age :"))
print ("Your age is :" , a)

if(a >= 18):
    print("You can drive")
    
else:
    print("You can't drive")
    
    
#     # Q1️⃣ Even / Odd Checker*****************************************
    
a = int(input("Enter number :"))
print("The number is :" , a)
     
if ( a % 2 == 0 ):
         print("even")
else :
         print("odd")

# # Q2️⃣ Biggest Number Finder*****************
# # User se 2 numbers lo:********************
# # Jo bada ho → print karo*********************

a = int(input("Enter first number : "))
b = int(input("Enter second number : "))

if (a>b) :
    print("Large number is first :" , a )
elif (b>a) :
 print("Large number is second :" , b )
else :
    print("Both are equal:")
    
    
# #     Q3️⃣ Simple ATM Logic 💰**************
# # User se balance lo:******************
# # ✔ balance >= 1000 → "Withdrawal Allowed"*****************
# # ✔ else → "Insufficient Balance"*********

num = int(input("Enter your balancce :"))

if (num >= 1000) :
    print("Withdrawal Allowed")
    
else :
    print("Insufficient Balance")
    
 
# # wrong & right password********************

password = input("Enter your password :")

if (password == "mohit123"):
    print ("Login succesfully") 
else:
    print("wrong password") 