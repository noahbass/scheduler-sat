import unittest
from main import cool_function


class SchedulerSATTEsts(unittest.TestCase):
    def test_cool_function(self):
        result = cool_function()
        self.assertEqual(result, 'something')


if __name__ == '__main__':
    unittest.main()
