# info = {"name" : "mohit", "class" : 12, "roll" : 1}
# print(info.keys())


# list = dict(Name = "Mohit ", classs = "b.tech sem 8", age = 21, loction = "pindatand")
# print(list)


# # 1️⃣ Student Info**********************************************************************************************
# # Ek dictionary banao:*****************************************************************************************
# # name, age, marks*********************************************************************************************


# dict = {"name": "mohit", "age": 21, "marks": 7.34}
# print(dict)   #["name"]


# # 2️⃣ Add New Key*************************************************************************************************
# # Dictionary me ek new key add karo:*****************************************************************************

# dict = {
#     "name": "mohit", 
#     "age": 21,
#     "marks": 7.34
#     }

# dict["city"] = "giridih"

# print("new dict :", dict)


# student = {
#     "name": "Mohit",
#     "age": 20,
#     "marks": 85
# }
# print(student)


# # 3️⃣ Update Value*****************************************************************************************************
# # Marks ko update karo.************************************************************************************************

# students = {
#     "name": "Mohit",
#     "age": 20,
#     "marks": 85
# }

# students["marks"] = 95
# print(students)


# # 4️⃣ Print All Keys*********************************************************************************************************
# # Saare keys print karo.*****************************************************************************************************


studentt = {
    "name": "Mohit",
    "age": 20,
    "marks": 85
}
studentt["marks"] = 95

print(studentt.keys())        #   all keys print

print(studentt.values())      #   all values print


# 6️⃣ Sum of Values*************************************************************************************************************
# Dictionary me numbers ho******************************************************************************************************
# Unka sum nikalo.**************************************************************************************************************


summ = {"a": 10, "b": 20, "c": 30}
print(sum(summ.values()))


# 7️⃣ Find Maximum Value*******************************************************************************************************
# Dictionary me se max value find karo.****************************************************************************************


summ = {"a": 10, "b": 20, "c": 30}
print(max(summ.values()))


# 8️⃣ Count Characters**********************************************************************************************************
# User se string lo************************************************************************************************************
# Har character ka count dictionary me store karo.*****************************************************************************


string = input("Enter your string :")

char_count = {}

for char in string:
    if char in char_count:
        char_count[char] += 1     # already exists -> count badao
        
    else:
        char_count[char] = 1      # naya character -> 1 se start karo
        
print("string :", string)
print("character count :", char_count)


# 9️⃣ Word Count**************************************************************************************************************
# Sentence lo****************************************************************************************************************
# Har word kitni baar aaya count karo.*****************************************************************************************


sentence = input("Enter your santence :")

word_count = {}

words = sentence.split()

for word in words:
    if word in word_count:
        word_count[word] += 1      # already exists → count badao
        
    else:
        word_count[word] = 1       # naya word → 1 se start
        
print("sentences :", sentence)
print("word counts :", word_count)


# 🔟 Key Exists Check*****************************************************************************************************
# User se key lo***********************************************************************************************************
# Check karo dictionary me exist karti hai ya nahi.************************************************************************


