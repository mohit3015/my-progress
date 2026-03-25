

# Pehle file create karo
file = open("mm.txt", "w")        
file.write("Hello! This is my file.")
file.close()

# file ke new line ko add karo
file= open("mm.txt", "a")
file.write("\nsecond line")            # Multiple Names Save: User se 3 line lo file me save karo
file.write("\nthird line")
file.write("\nfourth line")
file.close()

# file se specific line read karo
file = open("mm.txt", "r")
lines = file.readlines()
print("second line :", lines[1])
count = len(lines)                     # Count Lines (File me kitni lines hain count karo)
print("total lines :", count)
file.close()

# Phir file read karo
file = open("mm.txt", "r")  
content = file.read()
print("full content :", content)
file.close()


# Ek file me numbers likho:********************************************************************************
# 10
# 20
# 30
# Read karo aur total sum print karo*************************************************************************

file = open("number.txt", "w")
file.write("10\n20\n30\n40\n50")
file.close()

file = open("number.txt", "r")
lines = file.readlines()

total = 0
for line in lines:
    total += int(line)
    
print("Numbers :", lines)
print("Total of sum :", total)
file.close()


# STUDENT SAVE SYSTEM*************************************************************************************
# 1. Add Student******************************************************************************************
# 2. Show All Students*************************************************************************************
# 3 Search Student****************************************************************************************
# 4 Delete Student****************************************************************************************
# 3. Exit*************************************************************************************************

file = open("students.txt", "w")

while True:
    print("\n==== STUDENT SAVE SYSTEM =====")
    print("1. Add Student")
    print("2. Show Student")
    print("3. Search Student")
    print("4. Delete Student")
    print("5. Exit")
    
    choice = int(input("Enter your choice :"))
    
    # Option 1 - Add Student
    if choice == 1:
        name = input("Enter Name :")
        marks = input("Enter Marks :")
        
        file = open("students.txt", "a")
        file.write("Name : " + name + "| Marks : " + marks + "\n")
        file.close()
        print("Student Add Successfully!")
        
    # Option 2 - Show All Students
    elif choice == 2:
         print("\n===== ALL STUDENTS =====")
         file = open("students.txt", "r")
         lines = file.readlines()
        #  print(lines)
         file.close()
         
         if len(lines) == 0:
             print("No Any Student Add!")
             
         else:
             for i in range(len(lines)):
                 print("Students", i+1, ":", lines[i].strip())              # extra spaces/lines hatao
                 
     # Option 3 - Search Studen
    elif choice == 3:
        print("\n===== SEARCH STUDENT =====")
        search = input("Enter student name :")
        found = False
        
        file = open("students.txt", "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            if search.lower() in line.lower():
                print("Found!", "|", line.strip())
                found = True
                break
            if not found:
                print("Student not found!")
                
     # Option 4 - Delete Student
    elif choice == 4:
        print("\n===== DELETE STUDENT =====")
        search = input("Enter student name :")
        found = False
        
        file = open("students.txt", "r")
        lines = file.readlines()
        file.close()
        
        file = open("students.txt", "w")
        for line in lines:
            if search.lower() not in line.lower():
                file.write(line)
            else:
                found = True
        file.close()
            
        if found:
            print("Student Deleted successfully!")
                
        else:
            print("Student not found!")
                 
     # Option 5 - Exit
    elif choice == 5:
        print("\n==============================")
        print("👋 Goodbye! See you again!")
        print("==============================")
        exit()
        
    else:
        print("Invalid choice! Please select 1-3")
        
        
# Read Students*******************************************************************************************
# File se data read karo aur print karo********************************************************************
        
# File me students save karo
file = open("students.txt", "w")
file.write("Name : Mohit | Marks : 85\n")
file.write("Name : Rahul | Marks : 90\n")
file.write("Name : Priya | Marks : 78\n")
file.write("Name : Sulekha | Marks : 92\n")
file.close()

# File se data read karo
file = open("students.txt", "r")
lines = file.readlines()
# print(lines)
file.close()

# Print karo
print("===== ALL STUDENTS =====")
for i in range(len(lines)):
    print("Student", i+1, ":", lines[i].strip())
    
print("========================")
print("Total Students:", len(lines))


# Search in File*********************************************************************************************************
# User se name lo*********************************************************************************************************
# 👉 file me search karo (found / not found)******************************************************************************

file = open("students.txt", "w")
file.write("Name : Mohit | Marks : 85\n")
file.write("Name : Rahul | Marks : 90\n")
file.write("Name : Priya | Marks : 78\n")
file.write("Name : Sulekha | Marks : 92\n")
file.close()

file = open("students.txt", "r")
lines = file.readlines()
file.close()

search = input("Enter student name :")
found = False

for line in lines:
    if search.lower() in line.lower():
        print("found", line.strip())
        found = True
        break
    
else:
# if not found:
    print("not found")