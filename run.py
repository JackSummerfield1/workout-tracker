class Exercise:
    '''
    Creates an instance of Exercise
    '''
    def __init__(self, exercise_type, reps, weight):
        # Initialises attributes of specific exercise
        self.exercise_type = exercise_type
        self.reps = reps
        self.weight = weight

    def calculate_load(self):
        # Handles load calculation (Total weight lifted by the user)
        total_load = self.weight * self.reps
        return total_load
