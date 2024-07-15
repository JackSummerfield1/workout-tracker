from datetime import datetime


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
            break
            # Terminal breaks from the code once a valid date is entered
        else:
            print(f"The date entered ({date}) is invalid.")


def exercise_valid():
    exercise_type = input(
        'Please enter your desired exercise. (E.g. Push-up or Pull-up)\n')
    sets = int(
        input('Please enter the amount of sets you wish to complete. (E.g. 3)\n'))
    reps = int(input(
        'Please enter the amount of reps you wish to complete per set. (Must be in range: 6 - 15)\n'))
    weight = int(
        input('Please enter the weight being moved in kg. (E.g. 75)\n'))
    exercise_attr = Exercise(exercise_type, sets, reps, weight)
    print(f"Exercise Type: {exercise_attr.exercise_type}\n")
    print(f"Sets: {exercise_attr.sets}\n")
    print(f"Reps: {exercise_attr.reps}\n")
    print(f"Weight: {exercise_attr.weight}\n")
    print(f"Total Load: {exercise_attr.calculate_load()}")


def add_workout():
    '''
    Handles the user adding a workout to their program, including a variety of
    relevant attributes
    '''
    # date_valid()
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


# main()
add_workout()
