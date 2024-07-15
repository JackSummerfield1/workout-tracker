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


def main():
    '''
    Handles all functions and classes
    '''
    menu_decorator()


main()
