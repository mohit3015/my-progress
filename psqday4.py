
# help of time i print for loop count with 1 to 100*********************************8

# import time
# count = 0
# for i in range(100):
#     count = count+1
#     print(count, "project done")
#     time.sleep(0.5) #0.5 sedond take time to print each number 
    
    
    # ********************************
    
# for i in range(1 , 10):
#     print(i)
    
    # ********************************
    
# import time    
# count = 100
# while (count > 0) :
#     print(count)
#     count = count - 1
#     time.sleep(0.5)

# ****************************************

# num = int(input("Enter number: "))

# for i in range(1, 11):
#     print(num, "x", i, "=", num * i)
    
    
#     1️⃣ Print 1 to 10*********************************************
# While loop se 1 se 10 tak numbers print karo.*********************

count = 1
while (count <= 10):
    print(count)
    count = count + 1
    
# reverce**************************
count = 10
while (count >= 1):
    print(count)
    count = count - 1
    
# 3️⃣ Table Using While*************************************************************
# User se number lo aur uska table print karo (1 se 10 tak).**************************

num = int(input("Enter your number :"))
i = 1
while (i<=10):
    print(num, "x", i, "=" , num*i) 
    i= i+1
    
# 5️⃣ Sum of Digits*********************************
# User se number lo**********************************
# While loop se digits ka sum nikalo.***************************
# Example:****************************
# 123 → 1+2+3 = 6**************************

num = int(input("Enter your number: "))

total = 0          # Store sum here
temp = num         # Save original number

while temp > 0:
    digit = temp % 10      # Get last digit
    total = total + digit  # Add to total
    temp = temp // 10      # Remove last digit

print("Sum of digits:", total)


# 7️⃣ Prime Number (While Version)******************************
# User se number lo*****************************
# While loop se check karo prime hai ya nahi.*******************


num = int(input("Enter your number :"))

i = 2
is_prime = True

while (i < num):
    if num % i == 0:
        is_prime = False
        break
    i = i+1
if (num < 2):
    print("Not prime")
elif(is_prime):
    print(num , "Is prime")
else:
    print("Is not prime")
    
    
    
# 8️⃣ Factorial Using While************************
# User se number lo**********************************
# While loop se factorial nikalo.************************

num = int(input("Enter your number: "))

factorial = 1          # Store sum here
temp = num         # Save original number((copy of number))

while temp > 0:
    factorial = factorial * temp      # Multiply
    temp = temp - 1                   # Decrease by 1

print("Factorial of", num, "is :", factorial)


num = int(input("Enter your number"))

factorial = 1
temp = num
while temp > 0:
    factorial = factorial * temp
    temp = temp - 1
    
print("Factorial of is:", num, factorial)



# 🔵 Level 3 – Interesting Logic
# 9️⃣ Password Until Correct
# Password set karo: "python123"
# Jab tak user sahi password na dale
# Tab tak loop chalta rahe.


passward = "python123"

user_input = input("Enter your passward :")

while user_input != passward : 
    print("wrong passwaed try again")
    user_input = input("Enter your passward:")
    
print("Granted now access")



# 1️⃣1️⃣ ATM Program (Mini Project 💳)********************
# Balance = 10000**********************************
# Menu show karo:**********************************
# Check Balance**************************************
# Withdraw********************************************
# Exit************************************************
# Jab tak user Exit na kare****************************
# Loop chalta rahe.***************************************


pin = 45678
balance = 10000
attempts = 0
max_attempts = 3

print("=================================")
print("         WELCOME TO ATM          ")
print("=================================")

while attempts < max_attempts:
    entered_pin = int(input("\nEnter your PIN:"))
    
    if entered_pin == pin:
        print("PIN Correct! Access Granted!\n")
        break
    else:
        attempts = attempts + 1
        remaining = max_attempts - attempts
        
        if attempts == max_attempts:
            print("================================")
            print("     Today's limit crossed!     ")
            print("   Please try after 24 hours    ")
            exit()
        else:
            print(f"wrong PIN! You have {remaining} attempts(s) remaining.")


while True:
    print("\n=====ATM MENU=====")
    print("1. Check Balance")
    print("2. Withdraw")
    print("3. Exit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        print("your balance is" , balance)
        
    elif choice == 2:
        amount = int(input("Enter amount to withdraw: "))
        
        if amount > balance:
            print("Insufficient balance!")
            
        elif amount <= 0:
            print("Invalid amount!")
            
        else:
            balance = balance - amount
            print("Withdrawal successful!")
            print("Remaining balance:", balance)
            exit()
            
    elif choice == 3:
        print("\n============================")
        print("    Thank you for using ATM   ")
        print("          Goodbye!            ")
        print("==============================")
        exit()
        
    else:
        print("Invalid choice! Please select 1, 2 or 3")