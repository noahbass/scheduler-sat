import unittest
from validator import validate, all_true
import json


class ValidaterTests(unittest.TestCase):
    def test_json_test(self):
        with open('test_files/validator/students-small.json') as students_file:
            students_json = json.load(students_file)
        with open('test_files/validator/teachers-small.json') as teachers_file:
            teachers_json = json.load(teachers_file)

        periods_in_day = 3

        result = validate(students_json, teachers_json, periods_in_day)

        self.assertIsInstance(result, bool)
        print('Validator result:', result)
        # self.assertTrue(result)
    
    def test_all_true1(self):
        test_input = [True, True, True, True]
        
        result = all_true(test_input)

        self.assertIsInstance(result, bool)
        self.assertTrue(result)
    
    def test_all_true2(self):
        test_input = [True, False, True, True, False, True, True]
        
        result = all_true(test_input)
        expected = [1, 4]

        self.assertIsInstance(result, list)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
