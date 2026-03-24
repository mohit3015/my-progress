# 🔟 Mini Project (IMPORTANT)************************************************************************
# # Student Report System*****************************************************************************
# # Features:****************************************************************************************
# # Show all students**********************************************************************************
# # Add student****************************************************************************************
# # Search student***************************************************************************************
# # Exit**************************************************************************************************
# # 👉 While loop + dictionary + list combine***************************************************************


students = [ 
          {"name": "Mohit", "age": 21, "marks": 95},
          {"name": "Rahul", "age": 21, "marks": 85},
          {"name": "Priya", "age": 19, "marks": 78},
          {"name": "Sulekha", "age": 20, "marks": 96}
          ]

while True:
    print("\n==== STUDENT REPORT SYSTEM ====")
    print("1. Show All Students")
    print("2. Add Student")
    print("3. Search Student")
    print("4. Show Topper")
    print("5. Update Marks")
    print("6. Show Average Marks")
    print("7. Show Pass/Fail")
    print("8. Sort by Marks")
    print("9. Delete Student")
    print("10. Exit")
    
    choice = int(input("Enter your choice :"))
    
    
    # Option 1 - Show All Students
    if choice == 1:
        print("\n===== ALL STUDENTS =====")
        for s in students:
            print("Name :", s["name"],
                  "| Age :", s["age"],
                  "| Marks :", s["marks"]
                  )
           
            
    # Option 2 - Add Student
    elif choice == 2:
        print("\n===== ADD STUDENT =====")
        name = input("Enter name :")
        age = int(input("Enter age :"))
        marks = float(input("Enter marks :"))
        
        new_student = {
            "name": name,
            "age": age,
            "marks": marks
        }
        students.append(new_student)        # dict me add karo
        print("Student added successfully!")
        
        
    # Option 3 - Search Student
    elif choice == 3:
        print("\n===== SEARCH STUDENT =====")
        search = input("Enter student name :")
        found = False
        
        for s in students:
            if s["name"].lower() == search.lower():  # case insensitive
                print("Name :", s["name"],
                      "Age :", s["age"],
                      "Marks :", s["marks"]
                      )
                found = True
                break
            
        if not found:
            print("Student not found!")
       
            
    # Option 4 - Show Topper
    elif choice == 4:
        print("==== SHOW TOPPER ====")
        topper = students[0]
        for s in students:
            if s["marks"] > topper["marks"]:
                topper = s
        print("Topper:")
        print("Name:", topper["name"],
              "| Age:", topper["age"],
              "| Marks:", topper["marks"])
        
        
    #  Option 5 - Update Marks
    elif choice == 5:
        print("\n===== UPDATE MARKS =====")
        search = input("Enter student name: ")
        found  = False
        for s in students:
            if s["name"].lower() == search.lower():
                new_marks = float(input("Enter new marks: "))
                s["marks"] = new_marks
                print("Marks updated successfully!")
                found = True
                break
        if not found:
            print("Student not found!")
            
    
    
    # Option 6 - Show Average Marks
    elif choice == 6:
        print("\n===== AVERAGE MARKS =====")
        total = 0
        for s in students:
            total += s["marks"]
        average = total / len(students)
        print("📊 Average Marks:", average)
            
            
    # Option 7 - Show Pass/Fail
    elif choice == 7:
        print("\n===== PASS/FAIL =====")
        for s in students:
            if s["marks"] >= 50:
                print("Name:", s["name"],
                      "| Marks:", s["marks"], "| Pass")
            else:
                print("Name:", s["name"],
                      "| Marks:", s["marks"], "| Fail")
            

    # Option 8 - Sort by Marks
    elif choice == 8:
        print("\n===== SORT BY MARKS =====")
        sorted_students = sorted(students,
                                 key=lambda s: s["marks"],
                                 reverse=True)
        for s in sorted_students:
            print("Name:", s["name"],
                  "| Age:", s["age"],
                  "| Marks:", s["marks"])
      
            
     # Option 9 - Delete Student
    elif choice == 9:
        print("\n===== DELETE STUDENT =====")
        search = input("Enter student name: ")
        found  = False
        for s in students:
            if s["name"].lower() == search.lower():
                students.remove(s)
                print("Student deleted successfully!")
                found = True
                break
        if not found:
            print("Student not found!")
            
            
    # ✅ case insensitive
    elif choice == 10:
        print("\n==============================")
        print("👋 Goodbye! See you again!")
        print("==============================")
        exit()
        
    else:
        print("❌ Invalid choice! Please select 1-4")