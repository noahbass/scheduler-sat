import pandas as pd


# Validate the given students and teachers schedules
def validate(students_json, teachers_json, number_periods):
    students_df, teachers_df = pre_process(students_json, teachers_json)
    
    # Validation on number of periods
    if len(students_df.columns.values) != number_periods or \
       len(teachers_df.columns.values) - 1 != number_periods:
        print('Error: Expected number_periods and number of periods in the data to be equal in size')
        return False

    # Validation steps
    v1 = satisfy_condition_helper(validate_student_schedule_duplicates,
                                  students_df,
                                  'student',
                                  'student\'s classes should be unique')
    v2 = satisfy_condition_helper(validate_student_schedule_length,
                                  students_df,
                                  'student',
                                  'student\'s class count should be equal to number of periods',
                                  number_periods)
    v3 = satisfy_condition_helper(validate_student_schedule_is_full,
                                  students_df,
                                  'student',
                                  'student has no empty class periods')
    v4 = satisfy_condition_helper(validate_teacher_schedule_free,
                                  teachers_df,
                                  'teacher',
                                  'teacher has at least one empty class period')
    v5 = satisfy_condition_helper(validate_student_schedule_classes_offered,
                                  students_df,
                                  'student',
                                  'student\'s classes are offered in their time slots',
                                  teachers_df)
                                  
    # Validate that there are enough seats for each student
    v6 = validate_seats_for_students(students_df, teachers_df)

    print(v1, v1 == [])
    print(v2, v2 == [])
    print(v3, v3 == [])
    print(v4, v4 == [])
    print(v5, v5 == [])
    print(v6, v6 == True)

    # check if there were no errors
    return v1 == [] and \
           v2 == [] and \
           v3 == [] and \
           v4 == [] and \
           v5 == [] and \
           v6 == True


# Helper function: Take a function and apply it to each row
# of a DataFrame (extra arguements for calling the condition function
# are supported). Report back any errors.
def satisfy_condition_helper(condition_function, dataframe, target, message, *extra_args):
    result = [condition_function(row, *extra_args) for _, row in dataframe.iterrows()]
    result = all_true(result)

    if result != True:
        for error_index in result:
            print(f'Error: {target} {error_index+1} ({message})')

        return result

    # no errors
    return []


# Validate: that the student doesn't have duplicate classes in their schedule
def validate_student_schedule_duplicates(student_schedule):
    # get student's classes
    classes = student_schedule.values.tolist()
    classes_set = set(classes)
    
    # if the list and set are equal in length, then there are no duplicates
    return len(classes) == len(classes_set)


# Validate: that the student has exactly number_periods classes
def validate_student_schedule_length(student_schedule, number_periods):
    # get student's classes
    classes = student_schedule.values.tolist()

    # if the list and set are equal in length, then there are no duplicates
    return len(classes) == number_periods


# Validate: the student has no missing (None) classes
def validate_student_schedule_is_full(student_schedule):
    # get student's classes
    classes = student_schedule.values.tolist()
    
    if None in classes:
        # a student's schedule cannot have an empty slot
        return False

    return True


# Validate: the students classes are offered by at least one teacher
#           at the same time slot as the 
def validate_student_schedule_classes_offered(student_schedule, teachers_df):
    student_id = student_schedule.name # helpful for error messaging
    return_result = True

    # iterate over each period checking that each class is offered
    # at the correct period
    for period, class_name in student_schedule.iteritems():
        # get list of classes that are offered by in that period
        period_classes_offered = pd.Series(teachers_df[period]).values

        # check that each class is offered in each time slot
        if class_name not in period_classes_offered:
            print(f'Error: student {student_id} {class_name} not offered in {period}')
            return_result = False

    return return_result


# Validate: the teacher has at least 1 free period in their schedule
#           Note: A teacher with a null class at a specific period
#                 signifies that the teacher has a free period.
def validate_teacher_schedule_free(teacher_schedule):
    # get teachers's classes
    classes = teacher_schedule.values.tolist()
    
    if None in classes:
        return True

    return False


# Validate: for each period and each class period, there are
#           enough seats for every student
def validate_seats_for_students(students_df, teachers_df):
    result = True
    # iterate over dataframe columns (periods)
    # a huge imperative mess:
    for period_name in students_df:
        # group and aggregate (count) by column value
        students_period_df = students_df[period_name].groupby(students_df[period_name]).count()

        # for each column value, check which teachers are offering those
        # classes and what seat count they have
        for class_name, head_count in students_period_df.iteritems():
            # sum the classroom sizes for teachers offering this class
            # and in this period
            teacher_period = teachers_df[[period_name, 'classroomSize']]
            teacher_classrooms_sizes = teacher_period[teacher_period[period_name] == class_name].sum()['classroomSize']

            if head_count > teacher_classrooms_sizes:
                # the demand is larger then the number of seats available,
                # then the validation fails
                print(f'Error: {class_name} in {period_name} has {head_count} students, but only {teacher_classrooms_sizes} places')
                result = False

    return result


# Take JSON data and convert it to two DataFrames: one for teachers, one for students
def pre_process(students_json, teachers_json):
    students_df = pd.DataFrame(students_json)
    students_df = students_df.set_index('studentId')

    teachers_df = pd.DataFrame(teachers_json)
    teachers_df = teachers_df.set_index('teacherId')

    return students_df, teachers_df


# Returns True if every item in the list is true,
# otherwise, it returns the indexes that are not true.
def all_true(boolean_array):
    false_indexes = [index for index, item in enumerate(boolean_array) if item == False]

    if false_indexes == []:
        # everything is true
        return True
    
    # not everything is true: return the false indexes
    return false_indexes
