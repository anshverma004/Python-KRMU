# Name - Ansh Verma
# Date - 8 November 25
# Project title - Building a Calorie Tracking Console App

print("Welcome to the Daily Calorie Tracker CLI!")
print(
    "This tool helps you log your meals and calories, check your daily limit, and save a summary."
)

Meal_Names = []
Meal_Calories = []

Num_Meals = int(input("How many Meals do you want to log Today:"))

for i in range(Num_Meals):
    Meal_Name = input("Enter Meal Name:")
    Calorie_Amount = float(input("Enter Amount of Calorie:"))
    Meal_Names.append(Meal_Name)
    Meal_Calories.append(Calorie_Amount)

Total_Calories = sum(Meal_Calories)
Average_Calories = Total_Calories / Num_Meals

Calorie_Limit = float(input("Enter your Daily Calorie Limit:"))

if Average_Calories > Calorie_Limit:
    status_msg = "Warning! You've exceeded your daily calorie limit."
else:
    status_msg = "Congratulations! You stayed within your calorie limit today."

print("\nSummary Report")
print("Meal Name\tCalories")
print("-" * 25)
for meal, cal in zip(Meal_Names, Meal_Calories):
    print(f"{meal}\t\t{cal}")
print("-" * 25)
print(f"Total\t\t{Total_Calories}")
print(f"Average\t\t{Average_Calories:.2f}")
print(status_msg)
