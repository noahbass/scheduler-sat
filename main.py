import json
from itertools import chain
from constraint import *
from collections import Counter

# This function pre-processes the data that we are provided with
# Each student must have exactly as many required courses as there are periods in a day
# Each student must also have one and only one of each course in their required courses list
# Each teacher teaches exactly as many unique classes as there are periods in a day
def uniqueClasses(classList):
    return len(set(classList)) == len(classList)


def preprocess(periods_in_day, student_data, teacher_data):
    for student in student_data:
        if len(student["requiredClasses"]) != periods_in_day:
            return False
        if not uniqueClasses(student["requiredClasses"]):
            return False

    for teacher in teacher_data:
        if len(teacher["potentialClasses"]) != periods_in_day:
            return False
        if not uniqueClasses(teacher["potentialClasses"]):
            return False

    return True

def cool_function(periods_in_day, student_data, teacher_data):
    # Pre-process the data to assert data is ready for the CSP solver
    pre_process_result = preprocess(periods_in_day, student_data, teacher_data)
    if pre_process_result == False:
        print('Error - Number of classes for each student/teacher not equal to number of periods')
        exit(1)
    
    number_students = len(student_data)
    number_teachers = len(teacher_data)
    problem = Problem()

    print('student_data:', student_data)
    print('teacher_data:', teacher_data)

    # For each period in the students day, specify which classes they
    # can take. Then, for each period in a teachers day, specify which
    # classes they can teach.
    for period in range(1, periods_in_day + 1):
        for student in student_data:
            student_id = student['studentId']
            student_classes = student['requiredClasses']
            problem.addVariable(f'student{student_id}_period{period}', student_classes)

        for teacher in teacher_data:
            teacher_id = teacher['teacherId']
            teacher_classes = teacher['potentialClasses']
            problem.addVariable(f'teacher{teacher_id}_period{period}', teacher_classes)

    # for each studentx_periody class, there exists at least one
    # teacherz_periody offering that class.
    # Ensure that at least one teacher offers the class that each student needs
    def my_func(*argv):
        students_set = set()
        teachers_set = set()

        teacher_start_index = number_students + number_teachers - 1

        for index in range(0, len(argv)):
            if index >= teacher_start_index:
                # Add all classes a teacher is able to teach at a specific period
                teachers_set.add(argv[index])
            else:
                # Add all classes a student could potentially take at a specific period into the student set
                students_set.add(argv[index])

        # print('s:', students_set)
        # print('t:', teachers_set)
        for student_class in students_set:
            if student_class not in teachers_set:
                return False

        return True
    

    students_and_teachers = []
    for student in student_data:
        student_id = student['studentId']
        students_and_teachers += [f'student{student_id}']

    for teacher in teacher_data:
        teacher_id = teacher['teacherId']
        students_and_teachers += [f'teacher{teacher_id}']

    for period in range(1, periods_in_day + 1):
        # [f"student1_period1", f'student2_period1', f"teacher1_period1", ...]
        periods_students_and_teachers = [f'{identifier}_period{period}' for identifier in students_and_teachers]
        # print(students_and_teachers)
        # print('WHAT WE WANT:', periods_students_and_teachers)
        problem.addConstraint(FunctionConstraint(my_func), periods_students_and_teachers)

    # A student should take a class only once in a day
    # (but a teacher can teach the same class as many times as is neccessary)
    def allDifferent(*args):
        variables = list(args)
        if len(set(variables)) == len(variables):
            return True
        return False

    # Constraint: A student should take a class only once in a day
    for student in student_data:
        student_period_variables = []
        for period in range(1, periods_in_day + 1):
            student_id = student['studentId']
            student_period_variables += [f'student{student_id}_period{period}']
        problem.addConstraint(FunctionConstraint(allDifferent), student_period_variables)

    # Constraint: Teachers should not teach the same class at the same time
    for period in range(1, periods_in_day + 1):
        teacher_period_variables = []
        for teacher in teacher_data:
            teacher_id = teacher['teacherId']
            teacher_period_variables += [f'teacher{teacher_id}_period{period}']
        problem.addConstraint(FunctionConstraint(allDifferent), teacher_period_variables)

    solutions = problem.getSolutions()

    if solutions == []:
        print('no solution')
    else:
        print('solution:', solutions[0])

    return 'something'


def get_available_classes(student_data, teacher_data):
    student_classes = set(chain.from_iterable([student['requiredClasses'] for student in student_data]))
    teacher_classes = set(chain.from_iterable([teacher['potentialClasses'] for teacher in teacher_data]))

    if student_classes != teacher_classes:
        print('Error - Student and Teacher class lists do not match')
        exit(1)

    return student_classes


if __name__ == '__main__':
    with open('test_files/students.json') as students_file:
        students_json = json.load(students_file)
    with open('test_files/teachers.json') as teachers_file:
        teachers_json = json.load(teachers_file)

    periods_in_day = 1
    
    #print(students_json)
    #print(teachers_json)

    # get_available_classes(students_json, teachers_json)

    result = cool_function(periods_in_day, students_json, teachers_json)
    print('Hello, world')
