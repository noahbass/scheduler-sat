import unittest
from main import cool_function, get_available_classes
import json


class SchedulerSATTEsts(unittest.TestCase):
    # def test_cool_function(self):
    #     result = cool_function()
    #     self.assertEqual(result, 'something')

    def test_json_test(self):
        with open('test_files/scheduler/students.json') as students_file:
            students_json = json.load(students_file)
        with open('test_files/scheduler/teachers.json') as teachers_file:
            teachers_json = json.load(teachers_file)

        periods_in_day = 2
        
        #print(students_json)
        #print(teachers_json)

        # get_available_classes(students_json, teachers_json)

        result = cool_function(periods_in_day, students_json, teachers_json)


if __name__ == '__main__':
    unittest.main()
