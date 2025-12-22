import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "RK1"))
from main import *

class TestFileCatalogue(unittest.TestCase):
    def test_first_task(self):
        result = first_task(output=False)
        self.assertEqual(len(result["Archives"]), 2)
        self.assertEqual(result["Archives"][0].catalogue_id, 3)
    
    def test_second_task(self):
        result = second_task(output=False)
        self.assertEqual(result[0][1], 10240)
        self.assertEqual(result[1][1], 3072)
        self.assertEqual(result[2][1], 2048)
    
    def test_third_task(self):
        result = third_task(output=False)
        self.assertEqual(result[0][0].name, "Archives")
        self.assertEqual(result[0][1].size, 10240)
        self.assertEqual(result[-1][0].name, "User Files")
        self.assertEqual(result[-1][1].size, 512)

if __name__ == "__main__":
    unittest.main()
