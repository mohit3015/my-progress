
def geet():
    print("helo mohit")
    
geet()




# 1️⃣ Sum Function**********************************************************
# Function banao jo 2 numbers ka sum return kare.**************************

# a = 2
# b = 5
# def add(a,b):
#     return a + b
# print(add(a,b))

# # sub****************************

# c = 1
# d = 8
# def sub(c,d):
#     return c - d
# print(sub(c,d))


# 2️⃣ Even Odd Checker*****************************************************************
# Function banao jo check kare number even hai ya odd.**********************************


def check_odd_even(num):
    print("Your num is :",num)
    if num % 2 == 0:
        print("even")
        
    else:
        print("odd")
        
num = int(input("Enter your num:"))
check_odd_even(num)



# 3️⃣ Square Function*************************************************************
# Function banao jo number ka square return kare.**********************************

num = 4
def square(num):
    return num*num

num = int(input("Enter your num :"))
print("Your num square is",square(num))


# 4️⃣ Largest of Two Numbers**************************************************************
# Function banao jo 2 numbers me se bada number return kare.********************************

def check_large_num(num1,num2):
    print("Large num is :")
    
    if num1 > num2:
        print("num1 is large num", num1)
        
    elif num2 > num1:
        print("num2 is large num", num2)
        
    else:
        print("both are equal")
        
num1 = int(input("Enter your first num :"))
num2 = int(input("Enter your second num :"))     
(check_large_num(num1,num2))

# *******************************************

def largest(a,b):
    if a > b:
        return a
    else:
        return b
print("Largest num is :",largest(5,6))


# 5️⃣ Table Function********************************************************************
# Function banao jo number ka table (1–10) print kare.**********************************


def table(num):
    for i in range(1 , 11):
        print(num,"x",i, "=",num*i)
     
num = int(input("Enter your num :"))       
table(num)


# 6️⃣ Factorial Function*******************************************************
# Function banao jo number ka factorial calculate kare.***********************


def factorial(num):
    result = 1
    temp = num
    while temp > 0:
        result = result * temp
        temp = temp - 1
    
    print("factorial of",num, "is",result)
    
num = int(input("Enter your num :"))
factorial(num)


# 7️⃣ Reverse Number**********************************************
# Function banao jo number reverse kare.************************


def reverse_num(num):
    import time
    count = 100
    while (count >= 1):
        print(count)
        count = count - 1
        time.sleep(0.2)
reverse_num(num)

# ******************************************

def reverse_num(num):

    rev = 0

    while num > 0:
        digit = num % 10
        rev = rev * 10 + digit
        num = num // 10

    print("Reverse number:", rev)
    

# 8️⃣ Count Digits***************************************************************
# Function banao jo number me total digits count kare.***************************


def total_digits(num):
    total = 0
    temp = num
    
    while temp > 0:
        digits = temp % 10
        total = total + digits
        temp = temp // 10
        
    print("sum of total digits is :", total)
    
num = int(input("Enter your num :"))
total_digits(num)


# 9️⃣ Prime Number Function
# Function banao jo check kare number prime hai ya nahi.


def prime_num(num):
    i = 2
    is_prime = True
    
    while (i < num):
        if num % i == 0:
            is_prime = False
            break
        i = i + 1
        
    if (num < 2):
        print("not prime")
        
    elif (is_prime):
        print(num,"is prime")
        
    else:
        print("is not prime")
num = int(input("Enter your num :"))        
prime_num(num)    


# 🔟 Vowel Counter
# Function banao jo string me vowels count kare.


def vowel_counter(string):
    count = 0
    vowels = "aeiouAEIOU"    # all vowels
    
    for char in string:
        if char in vowels:
            count = count + 1
    
    print("String:", string)
    print("Vowel count:", count)

string = input("Enter your string: ")
vowel_counter(string)