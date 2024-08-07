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
    print('\nPlease select one of the following options (1-5)...\n')
    print('1. Add Workout\n')
    print('2. View Last 5 Workouts\n')
    print('3. Edit Workout\n')
    print('4. Delete Workout\n')
    print('5. Exit\n')
    print('*' * 35)
    # Code above is simply decoration to the terminal menu


def edit_menu_decorator():
    print('*' * 35)
    print('\nPlease select which attribute you wish to change (1 - 6):\n')
    print('1. Date\n')
    print('2. Exercise Type\n')
    print('3. Sets\n')
    print('4. Reps\n')
    print('5. Weight\n')
    print('6. Exit Editor\n')
    print('*' * 35)
    # Code above is simply decoration for the terminal menu in the editor func


def valid_date(date):
    '''
    Handles date validation, ensures a correct date is
    entered in the provided format
    Credit to Max O'Didily with help on this:
    https://www.youtube.com/watch?v=5n_JagFqWeg
    '''
    try:
        datetime.strptime(date, '%d/%m/%Y')
        # Ensures date is valid and in correct format
        return True
    except ValueError:
        return False


def validate_exercise_type():
    '''
    Handles data validation, specifically the exercise_type attr
    '''
    while True:
        # Ensures a valid exercise is provided,
        # no integers or strings longer than 16 char
        exercise_type = input(
            'Please enter your desired exercise. (E.g. Pushup or Pullup)\n')
        if len(exercise_type) <= 16 and exercise_type.isalpha():
            print(f"The exercise type ({exercise_type}) is valid.")
            return exercise_type
        else:
            print('Invalid input. Please enter a valid exercise type.')


def validate_sets():
    '''
    Handles data validation, specifically the sets attr
    '''
    while True:
        # Ensures a valid amount of sets are provided,
        # must be a feasible integer between 1 and 5
        try:
            sets = int(
                input('Please enter the amount of sets '
                      'you wish to complete. (E.g. 3)\n'))
            if sets <= 5 and sets > 0:
                # Ensures value entered is within correct range
                print(f"The sets ({sets}) are valid.")
                return sets
            else:
                print('Invalid input. Please enter a number between 1 - 5.')
        except ValueError:
            print('Value entered is invalid.')


def validate_reps():
    '''
    Handles data validation, specifically the reps attr
    '''
    while True:
        # Ensures a valid amount of reps are allocated,
        # must be a reasonable integer in range 6 - 15
        try:
            reps = int(input(
                'Please enter the amount of reps you wish to complete per set.'
                ' (Must be in range: 6 - 15)\n'))
            if reps <= 15 and reps >= 6:
                # Ensures value entered is in correct range
                print(f"The reps ({reps}) are valid.")
                return reps
            else:
                print('Invalid input. Please enter a '
                      'valid number between 6 - 15.')
        except ValueError:
            print('Value entered is invalid.')


def validate_weight():
    '''
    Handles data validation, specifically the weight attr
    '''
    while True:
        # Ensures a valid weight is specified, must be humanely possible,
        # hence the range provided (1 - 500kg)
        try:
            weight = int(
                input('Please enter the weight '
                      'being moved in kg. (E.g. 75)\n'))
            if weight <= 500 and weight > 0:
                # Ensures value entered is in correct range
                print(f"The weight ({weight}) is valid.")
                return weight
            else:
                print('Invalid input. Please enter a number between 1 - 500.')
        except ValueError:
            print('Value entered is invalid.')


def date_insert():
    '''
    Handles correct date entered, loops back through
    if incorrect date is entered.
    '''
    while True:
        # While loop used so that if user input is invalid, the code loops
        # back through until valid date entered
        date = input(
            'Please enter a date for this workout in the format DD/MM/YYYY.\n')

        valid_date(date)

        if valid_date(date):
            print(f"The date entered ({date}) is valid.")
            row.insert(0, date)
            # Inserts date attr at correct column on google sheet, (ind 0)
            break
            # Terminal breaks from the code once a valid date is entered
        else:
            print(f"The date entered ({date}) is invalid.")


def exercise_insert():
    '''
    Handles all exercises attributes, ensuring all data input is valid and
    abides by the boundaries set.
    '''
    exercise_type = validate_exercise_type()
    sets = validate_sets()
    reps = validate_reps()
    weight = validate_weight()

    row.insert(1, exercise_type)
    row.insert(2, sets)
    row.insert(3, reps)
    row.insert(4, weight)
    # Insert the row into the Google Sheet

    exercise_attr = Exercise(exercise_type, sets, reps, weight)
    print(f"Exercise Type: {exercise_attr.exercise_type.capitalize()}\n")
    print(f"Sets: {exercise_attr.sets}\n")
    print(f"Reps: x{exercise_attr.reps}\n")
    print(f"Weight: {exercise_attr.weight}kg\n")
    print(f"Total Load: {exercise_attr.calculate_load()}kg")
    # Prints to the user exactly what they have entered to be sent
    # to the google worksheet


def assign_workout_num():
    '''
    Handles assigning a number to each workout, this allows
    for specific workouts to be targeted later on during the edit
    and delete processes
    '''
    data = workouts.get_all_values()
    num = len(data) - 1
    row.insert(6, num)


def save_workout():
    '''
    Handles all data inputted being inserted into the google sheet
    '''
    print('*' * 35)
    print('\nSaving workout to google sheet...\n')
    workouts.append_row(row)
    print('Workout has been successfully saved!\n')
    print('*' * 35)


def add_workout():
    '''
    Handles the user adding a workout to their program, including a variety of
    relevant attributes
    '''
    date_insert()
    exercise_insert()
    assign_workout_num()
    save_workout()


def view_workouts():
    '''
    Handles printing to the terminal the last 5 workouts in the google sheet
    '''
    all_workout_rows = workouts.get_all_values()
    # Gathers all of the workouts from the google sheet
    last_five_rows = all_workout_rows[-5:]
    # Collates the last 5 workout entries made to the google sheet]
    heading = 'Date:, Exercise Type:, Sets:, Reps:, Weight:, '
    'Total Load:, Number:\n'
    print('\nThe 5 most recent workouts in your Google '
          'sheet are as follows:\n')
    print(heading)
    for row in last_five_rows:
        # Iterates through each item in the row and ensures that they
        # have even amount of whitespace per category
        print(f"{row[0]}, {row[1] + (16 - len(row[1])) * ' '}, "
              f"{row[2] + (2 - len(row[2])) * ' '},"
              f"{row[3] + (2 - len(row[3])) * ' '}, "
              f"{row[4] + (3 - len(row[4])) * ' '}, "
              f"{row[5] + (4 - len(row[5])) * ' '}, {row[6]}")


def edit_workout():
    '''
    Handles workouts to be edited, selection done through workout number
    '''
    data = workouts.get_all_values()
    # Gathers all data in the worksheet

    wk_num = 0

    while True:
        try:
            choice = int(input(
                f"Please enter the number of the workout you wish to edit, "
                f"num should be in range 0 - {len(data) - 2}\n"))
            if choice == 0 or (choice <= (len(data) - 2) and choice >= 0):
                # Allows user to choose a workout number in the correct range
                print(f"You have selected workout: {choice}\n")
                # Informs the user which workout they
                # have selected to be edited
                wk_num = wk_num + choice
                break
            else:
                continue
        except ValueError:
            print('Input is invalid, please try again')

    wk_to_edit = data[wk_num + 1]
    # Obtains the correct workout that the user wants to edit
    print(wk_to_edit)

    print('*' * 35)
    print('\nWelcome to ASUMA Workout Editor\n')

    while True:
        edit_menu_decorator()
        user_input = input('\nSelect an option, 1 - 6:\n\n')
        match user_input:
            case '1':
                while True:
                    # While loop used so that if user input is invalid,
                    # the code loops back through until valid date entered
                    new_date = input(
                        'Please enter the new date for this workout in the'
                        ' format DD/MM/YYYY.\n')

                    valid_date(new_date)

                    if valid_date(new_date):
                        # Ensures a valid date has been entered and then
                        # pushed to the google sheet
                        workouts.update_cell(wk_num + 2, 1, new_date)
                        print(f"The date for workout {wk_num} "
                              f"has been changed to {new_date}")
                        break
                    else:
                        print(f"The date entered ({new_date}) is invalid.")
            case '2':
                while True:
                    # Ensures a valid exercise is provided, no integers or
                    # strings longer than 16 char
                    new_exercise_type = input(
                        'Please enter your new exercise.\n')
                    if (len(new_exercise_type) <= 16
                            and new_exercise_type.isalpha()):
                        workouts.update_cell(wk_num + 2, 2, new_exercise_type)
                        print(f"The exercise type for workout {wk_num} "
                              f"has been changed to {new_exercise_type}")
                        break
                    else:
                        print('Invalid input. '
                              'Please enter a valid exercise type.')
            case '3':
                while True:
                    # Ensures a valid amount of sets are entered
                    try:
                        new_sets = int(
                            input(
                                'Please enter the desired '
                                'sets for this exercise:\n'))
                        if new_sets <= 5 and new_sets > 0:
                            workouts.update_cell(wk_num + 2, 3, new_sets)
                            print(f"The sets for workout {wk_num} "
                                  f"has been changed to {new_sets}")
                            break
                        else:
                            print(
                                'Invalid input. Please enter a '
                                'number between 1 - 5.')
                    except ValueError:
                        print('Value entered is invalid.')
            case '4':
                while True:
                    # Ensures a valid amount of reps are allocated, must be a
                    # reasonable integer in range 6 - 15
                    try:
                        new_reps = int(input(
                            'Please enter the new amount of reps you wish'
                            ' to complete per set. '
                            '(Must be in range: 6 - 15)\n'))
                        if new_reps <= 15 and new_reps >= 6:
                            workouts.update_cell(wk_num + 2, 4, new_reps)
                            new_total_load = new_reps * int(wk_to_edit[4])
                            workouts.update_cell(wk_num + 2, 6, new_total_load)
                            print(f"The reps for workout {wk_num} "
                                  f"has been changed to {new_reps} and"
                                  f" the new total load is {new_total_load}")
                            break
                        else:
                            print(
                                'Invalid input. Please enter a valid'
                                ' number between 6 - 15.')
                    except ValueError:
                        print('Value entered is invalid.')
            case '5':
                while True:
                    # Ensures a valid weight is specified, must be
                    # humanely possible, hence the range provided (1 - 500kg)
                    try:
                        new_weight = int(
                            input('Please enter the weight being moved in kg.'
                                  ' (E.g. 75)\n'))
                        if new_weight <= 500 and new_weight > 0:
                            workouts.update_cell(wk_num + 2, 5, new_weight)
                            new_total_load = new_weight * int(wk_to_edit[3])
                            workouts.update_cell(wk_num + 2, 6, new_total_load)
                            print(f"The weight for workout {wk_num} "
                                  f"has been changed to {new_weight} and"
                                  f" the new total load is {new_total_load}")
                            break
                        else:
                            print(
                                'Invalid input. Please enter a '
                                'number between 1 - 500.')
                    except ValueError:
                        print('Value entered is invalid.')
            case '6':
                break
            case _:
                print('Invalid option, please choose another operation.')


def del_workout():
    data = workouts.get_all_values()
    while True:
        try:
            choice = int(input(
                f"Please enter the number of the workout you wish to delete,"
                f" num should be in range 0 - {len(data) - 2}\n"))
            if choice == 0 or (choice <= (len(data) - 2) and choice >= 0):
                # Allows user to choose a workout number in the correct range
                print(f"You have selected workout: {choice}\n")
                # Informs the user which workout they
                # have selected to be edited
                break
            else:
                print('Input must be within the appropriate range, '
                      'stated above.')
                continue
        except ValueError:
            print('Input is invalid, please try again')

    if choice:
        # Handles deleting the row the user requests to be deleted
        workouts.delete_rows(choice + 2)

        print('*' * 35)
        print('\nWorksheet is being updated...\n')

        for row in data[choice + 2:]:
            # Decreases each workout number by 1,
            # that comes after the one to be deleted
            new_wk_num = int(row[6]) - 1
            workouts.update_cell(int(row[6]) + 1, 7, new_wk_num)

        print('Worksheet has been updated successfully.\n')
        print('*' * 35)


def user_choice():
    '''
    Handles the users choice on what they want to do,
    ie. add, edit, view or delete workouts.
    Use of a while loop to ensure the value entered is a number between 1-5,
    any values out of this range
    causes an error message to be displayed and the
    code is reiterated through the while loop.
    '''
    while True:
        menu_decorator()
        # Makes sure a valid option must be entered
        user_input = input('\nSelect an option, 1 - 5:\n\n')
        # Credit to:
        # https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
        # Using a match-case scenario instead of if else to improve performance
        match user_input:
            case '1':
                add_workout()
            case '2':
                view_workouts()
            case '3':
                edit_workout()
            case '4':
                del_workout()
            case '5':
                break
            case _:
                print('Invalid option, please choose another operation.')


def main():
    '''
    Handles all functions and classes
    '''
    print('*' * 35)
    print('\nWelcome to ASUMA Fitness Tracker\n')
    print('*' * 35)
    user_choice()


# This ensures main() runs only when the script is executed directly
if __name__ == '__main__':
    main()
