

l = [12, 13, 45, 65, 67, 89]
print(l)                    # print list       

# in list add one item**************************************************************************

l = [12, 13, 45, 65, 67, 89]
l.append(34)                  
print(l)                    # in list a method

# remove one item*******************************************************************************

l = [12, 13, 45, 34, 65, 67, 89]
l.remove(34)                   
print(l)                     # in list a method

# in 0 index element print************************************************************************************

l = [12, 13, 45, 65, 67, 89]
print(l[0])                  # in list a method

# print index positin of 89****************************************************************************

l = [12, 13, 45, 65, 67, 89]
print(l.index(89))           # in list a method

# ***************************************************************************************

marks = [85, 90, 78, 92]

for m in marks:
    print(m)
    
l = [12, 13, 45, 65, 67, 89]

print(len(l))

print(l[5])

for i in l:
    print(i) 


marks = [80, 90, 100]
total = 0

for m in marks:
    total += m
    print(m)

print("Total:", total)


# Q1️⃣****************************************************************************
# Ek list banao:******************************************************************
# [10, 20, 30, 40, 50]************************************************************
# ✔ Loop se sab print karo*******************************************************


item = [10, 20, 30, 40, 50]

for i in item:
    print(i)
    

# 2️⃣ Sum of List list = [10, 20, 30, 40, 50]**************************************
# List ke sab numbers ka sum nikalo.***********************************************


work = [10, 20, 30, 40, 50]

total = 0

for n in work:
    total += n
    print(n)
    
print("total", total)


# 3️⃣ Largest Number list = [10, 20, 30, 40, 50]************************************
# List me se sabse bada number find karo.*******************************************


find = [10, 20, 30, 40, 50]

find = [45, 31, 23, 56, 78, 1, 100]

# def largestnum(find):
    
largest = find[0]
    
for j in find:
    if j > largest:
        largest = j
    
print("lagest num of this list :", largest)
    
# largestnum(find)


# 4️⃣ Count Even Numbers***************************************************
# List me kitne even numbers hain count karo.*****************************


findevenn = [45, 31, 23, 56, 78, 1, 100]

count = 0 

for n in findevenn:
    if n % 2 == 0:
        count += 1
    
print("count of even num :", count)


# 5️⃣ Reverse List**********************************************************
# List ko reverse print karo.***********************************************


reverselist = [45, 31, 23, 56, 78, 1, 100]

reverselist.reverse()                     # .reverse is a method
print(reverselist)


# 6️⃣ User Input List*********************************************************
# User se 5 numbers lo aur list me store karo.********************************


addnum = [45, 31, 23, 56, 78, 1, 100]

m =[111,32, 44, 99]
addnum.extend(m)                      # .extend is method    
print(addnum)


# 7️⃣ Search Element**************************************************************
# List me koi number search karo (found / not found).*****************************


lll = [45, 31, 23, 56, 78, 1, 100]

n = int(input("enter your num :"))

if n in lll:
    print(n ,"found")
    
else:
    print(n, "not found")
    
    
# 8️⃣ Remove Duplicates***************************************************************
# List me se duplicate elements hatao.************************************************


ddd = [45, 31, 31, 23, 56, 78, 1, 100, 100]

print("Orginal list :", ddd)
print("New list :", list(set(ddd)))                # print(list(set(argument))) is method    


# 9️⃣ Merge Two Lists********************************************************************
# 2 lists ko combine karo.***************************************************************


mmm = [45, 31, 31, 23, 56, 78, 1, 100, 100]

nnn = [45, 31, 23, 56, 78, 1, 100]

k = mmm + nnn

print(k)


# 🔟 Average of List************************************************************************
# List ka average nikalo.********************************************************************


aaa = [45, 31, 23, 56, 78, 1, 100]

# print("Average", sum(aaa)/len(aaa))
print("list :", aaa)
total = 0 
for n in aaa:
    total += n

average = total / len(aaa)

print( "total :", total)
print("average :", average)


# 1️⃣ Second Largest Number*********************************************************************
# List me se second largest number find karo.****************************************************


ll = [45, 31, 23, 56, 78, 1, 100]

largest = ll[0]
second_largest = ll[0]

for n in ll:
    if n > largest:
        second_largest = largest 
        largest = n
        
print("list", ll)
print("largest :", largest)
print("second_largest :", second_largest)

# ************************************************
ll = [45, 31, 23, 56, 78, 1, 100]
ll.sort()
print("Second Largest:", ll[-2])


# 2️⃣ Count Frequency*********************************************************************************
# List me har element kitni baar aaya hai count karo**************************************************


ccc = [1, 2, 3, 4, 5, 3, 3, 3, 4, 4,2 ,4, 5, 5, 1, 2, 1, 2]
# print(ccc)

n = int(input("Enter num :"))

print(ccc.count(n), "times")

# unique = set(ccc)

# for n in unique:
#     print(n, "->" , ccc.count(n),"times")
    
    
# 3️⃣ Remove Negative Numbers***************************************************************************
# List me se sab negative numbers hatao.****************************************************************


bbb = [1, 2, -3, 4, 5, 3, -3, 3, 4, -4,2 ,4, 5, 5, 1, 2, -1, 2]

print("orginal list :",bbb)

new_list = []

for n in bbb:
    if n > 0:
        new_list.append(n)
        
print("new list :", new_list)


# 4️⃣ Find Common Elements***********************************************************************************
# Do lists lo aur common elements find karo.*****************************************************************


eee = [1, 2, 3, 4, 5, 3, 3, 3, 4, 4,2 ,4, 5, 5, 1, 2, 1, 2]
fff = [1, 3, 4, 5, 6, 3, 2, 1, 7, 6, 6, 5, 5, 4]

common = []
print("list :", eee)
print("list :", fff)
for n in eee:
    if n in fff and n not in common:
        common.append(n)
        
print("common list :", common)

common = list(set(eee) & set(fff))
print("common list :", common)


# 5️⃣ Sort Without sort()**************************************************************************************
# List ko ascending order me sort karo************************************************************************
# 👉 without using .sort()************************************************************************************


sss = [45, 31, 23, 56, 78, 1, 100]

print("orginal list :", sss)

for i in range(len(sss)):
    for j in range(i+1, len(sss)):
        if sss[i] > sss[j]:
            sss[i], sss[j] = sss[j], sss[i]
            
print("swap list :", sss)


# 6️⃣ Find Missing Number*************************************************************************************
# List me numbers 1–10 hone chahiye***************************************************************************
# Ek missing hai → usko find karo.*****************************************************************************
# Example:*****************************************************************************************************
# [1,2,3,4,6,7,8,9,10]*****************************************************************************************
# Missing → 5**************************************************************************************************


ggg = [1, 2, 3, 5, 7, 8, 9, 10, 11]

print("orginal list", ggg)

for i in range(1, 11):
    if i not in ggg:
        print("messing element :", i)


# 7️⃣ Palindrome ***************************************************************************************************
# Check karo list same forward & backward hai ya nahi.*************************************************************
# Example:*********************************************************************************************************
# [1,2,3,2,1] → Palindrome******************************************************************************************



        
        
# 8️⃣ Separate Even & Odd****************************************************************************************
# List ko 2 lists me divide karo:**********************************************************************************
# 👉 Even list****************************************************************************************************
# 👉 Odd list******************************************************************************************************


ee = [12, 13, 17, 34, 89, 44, 21, 31, 56, 76, 0, 22, 51]

print("orginal list :", ee)
even = []
odd = []

for n in ee:
    if n % 2 == 0:
        even.append(n)
        
    else:
        odd.append(n)
        
print(" even list :",even, "\n odd list :", odd)


# 9️⃣ Multiply All Elements******************************************************************************************
# List ke sab elements ka product nikalo.****************************************************************************


mm = [12, 13, 17, 34, 89, 44, 21, 31, 56, 76, 22, 51]

print("list :", mm)
total = 1
for n in mm:
    total *= n
    
print("total", total)


# 🔟 Remove Duplicates (Advanced)************************************************************************************
# Duplicate remove karo without using set()***************************************************************************


dd = [1, 2, 3, 4, 5, 3, 3, 3, 4, 4,2 ,4, 5, 5, 1, 2, 1, 2]

print("orginal list :", dd)

new_list = []

for n in dd:
    if n not in new_list:
        new_list.append(n)
        
print("new_list :", new_list)