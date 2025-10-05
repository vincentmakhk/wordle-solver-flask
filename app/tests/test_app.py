import unittest
from app import calculate_state

class TestCalculateStateFunction(unittest.TestCase):

    def test_calculate_state_cases(self):
        test_data = [
            ("ababa", "aaaaa", ["Green", "Gray", "Green", "Gray", "Green"]),
            ("bccbe", "abcde", ["Yellow", "Gray", "Green", "Gray", "Green"]),
            ("cbaba", "ababc", ["Yellow", "Green", "Green", "Green", "Yellow"]),
            ("eaaba", "abcda", ["Gray", "Yellow", "Gray", "Yellow", "Green"]),
            ("eadbc", "abcda", ["Gray", "Yellow", "Yellow", "Yellow", "Yellow"]),
        ]
        
        for input, answer, expected in test_data:
            with self.subTest(input=input, answer=answer, expected=expected):
                result = calculate_state(input, answer)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
