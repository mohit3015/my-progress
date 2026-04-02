
# # condition use

# import requests
# import json

# query = input("What type of news are you interested in: ")

# url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey=b3c56ff1bb614ba093ec19319ff6594a"

# r    = requests.get(url)
# news = json.loads(r.text)

# # Pehle status check karo
# print("\nStatus:", news["status"])
# print("Total Results:", news["totalResults"])
# print("-----------------------------------------")
        
# if news["totalResults"] == 0:
#     print("No news found!")
# else:
#     for i, article in enumerate(news["articles"]):
#         print("\nNews", i+1)
#         print("Title      :", article["title"])
#         print("Description:", article["description"])
#         print("------------------------------------------------")


# # while loop use

# import requests
# import json

# while True:
#     print("\n=== NEWS MENU ===")
#     print("1. Search news")
#     print("2. Exit")
    
#     choice = int(input("Enter your choice :"))
    
# # Option 1 - Search News
#     if choice == 1:
#         query = input("What type of news are you interested in: ")

#         url = f"https://newsapi.org/v2/everything?q={query}&from=2026-04-01&sortBy=publishedAt&apiKey=b3c56ff1bb614ba093ec19319ff6594a"

#         r    = requests.get(url)
#         news = json.loads(r.text)

#         # Pehle status check karo
#         print("\nStatus:", news["status"])
#         print("Total Results:", news["totalResults"])
#         print("-----------------------------------------")
        
#         if news["totalResults"] == 0:
#             print("No news found!")
#         else:
#             for i, article in enumerate(news["articles"]):
#                 print("\nNews", i+1)
#                 print("Title      :", article["title"])
#                 print("Description:", article["description"])
#                 print("------------------------------------------------")
#     elif choice == 2:
#         exit()
#     else:
#         print("Invalid choice! Please select 1-2")
        
        
import time
from plyer import notification

def water_reminder():
    while True:
        # Desktop notification
        notification.notify(
            title    = "Drink Water Reminder!",
            message  = "Time to drink water! Stay hydrated!",
            app_name = "Water Reminder",
            timeout  = 10        # 10 seconds dikhega
        )
        print("Drink Water Reminder sent!")
        print("Next reminder in 1 hour...")
        print("----------------------------------")
        
        time.sleep(7200)         # 2 hour = 7200 seconds

# Program start karo
print("===== WATER REMINDER STARTED =====")
print("You will be reminded every 2 hour!")
print("Press Ctrl+C to stop")
print("----------------------------------")
water_reminder()