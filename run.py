import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workout_tracker')

workouts = SHEET.worksheet('workouts')

row = []
# List of data to be sent to google sheet


class User:
    '''
    Creates an instance of User
    '''

    def __init__(self, username, age, height, weight):
        self.username = username
        self.age = age
        self.height = height
        self.weight = weight


class Exercise:
    '''
    Creates an instance of Exercise
    '''

    def __init__(self, exercise_type, sets, reps, weight):
        # Initialises attributes of specific exercise
        self.exercise_type = exercise_type
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def calculate_load(self):
        # Handles load calculation (Total weight lifted by the user)
        total_load = self.weight * self.reps
        row.insert(5, total_load)
        # Inserts total_load attr at correct column on google sheet, (ind 5)
        return total_load


def menu_decorator():
    print('*' * 35)
    print('\nWelcome to ASUMA Fitness Tracker\n')
    print('*' * 35)
    print('\nPlease select one of the following options (1-5)...\n')
    print('1. Add Workout\n')
    print('2. View Workouts\n')
    print('3. Edit Workout\n')
    print('4. Delete Workout\n')
    print('5. Exit\n')
    print('*' * 35)
    # Code above is simply decoration to the terminal menu


def date_valid():
    '''
    Handles correct date entered, loops back through if incorrect date is entered.
    '''
    while True:
        # While loop used so that if user input is invalid, the code loops back through until valid date entered
        date = input(
            'Please enter a date for this workout in the format DD/MM/YYYY.\n')

        def is_date(date):
            '''
            Handles date validation, ensures a correct date is entered in the provided format
            Credit to Max O'Didily with help on this: https://www.youtube.com/watch?v=5n_JagFqWeg
            '''
            try:
                date_object = datetime.strptime(date, '%d/%m/%Y')
                # Ensures date is valid and in correct format
                return True
            except ValueError:
                return False

        if is_date(date):
            print(f"The date entered ({date}) is valid.")
            row.insert(0, date)
            # Inserts date attr at correct column on google sheet, (ind 0)
            break
            # Terminal breaks from the code once a valid date is entered
        else:
            print(f"The date entered ({date}) is invalid.")


def exercise_valid():
    '''
    Handles all exercises attributes, ensuring all data input is valid and
    abides by the boundaries set.
    '''
    while True:
        # Ensures a valid exercise is provided, no integers or strings longer than 16 char
        exercise_type = input(
            'Please enter your desired exercise. (E.g. Pushup or Pullup)\n')
        if len(exercise_type) <= 16 and exercise_type.isalpha():
            row.insert(1, exercise_type)
            # Inserts exercise_type attr at correct column on google sheet, (ind 1)
            break
        else:
            continue

    while True:
        # Ensures a valid amount of sets are provided, must be a feasible integer between 1 and 5
        try:
            sets = int(
                input('Please enter the amount of sets you wish to complete. (E.g. 3)\n'))
            if sets <= 5 and sets > 0:
                row.insert(2, sets)
                # Inserts sets attr at correct column on google sheet, (ind 2)
                break
            else:
                continue
        except ValueError:
            print('Value entered is invalid.')

    while True:
        # Ensures a valid amount of reps are allocated, must be a reasonable integer in range 6 - 15
        try:
            reps = int(input(
                'Please enter the amount of reps you wish to complete per set. (Must be in range: 6 - 15)\n'))
            if reps <= 15 and reps >= 6:
                row.insert(3, reps)
                # Inserts reps attr at correct column on google sheet, (ind 3)
                break
            else:
                continue
        except ValueError:
            print('Value entered is invalid.')

    while True:
        # Ensures a valid weight is specified, must be humanely possible, hence the range provided (1 - 500kg)
        try:
            weight = int(
                input('Please enter the weight being moved in kg. (E.g. 75)\n'))
            if weight <= 500 and weight > 0:
                row.insert(4, weight)
                # Inserts weight attr at correct column on google sheet, (ind 3)
                break
            else:
                continue
        except ValueError:
            print('Value entered is invalid.')

    exercise_attr = Exercise(exercise_type, sets, reps, weight)
    print(f"Exercise Type: {exercise_attr.exercise_type.capitalize()}\n")
    print(f"Sets: {exercise_attr.sets}\n")
    print(f"Reps: x{exercise_attr.reps}\n")
    print(f"Weight: {exercise_attr.weight}kg\n")
    print(f"Total Load: {exercise_attr.calculate_load()}kg")

def add_workout():
    '''
    Handles the user adding a workout to their program, including a variety of
    relevant attributes
    '''
    date_valid()
    exercise_valid()


def user_choice():
    '''
    Handles the users choice on what they want to do, ie. add, edit, view or delete workouts.
    Use of a while loop to ensure the value entered is a number between 1-5, any values out of this range
    causes an error message to be displayed and the code is reiterated through the while loop.
    '''
    while True:
        # Makes sure a valid option must be entered
        user_input = input('\nSelect an option, 1 - 5:\n\n')
        if user_input == '1':
            break
        elif user_input == '2':
            break
        elif user_input == '3':
            break
        elif user_input == '4':
            break
        elif user_input == '5':
            break
        else:
            print('Invalid option, please choose another operation.')


def main():
    '''
    Handles all functions and classes
    '''
    menu_decorator()
    user_choice()


main()
