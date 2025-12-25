import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lab3", "lab_python_fp"))
from field import field
from unique import Unique
from gen_random import gen_random

class TestField(unittest.TestCase):
    def test_single_field_extraction(self):
        data = [
            {'title': 'Ковер', 'price': 2000, 'color': 'green'},
            {'title': 'Диван для отдыха', 'color': 'black'},
            {'color': 'blue'}
        ]
        result = field(data, "title")
        answer = ["Ковер", "Диван для отдыха"]
        self.assertEqual(result, answer)
    
    def test_multiple_fields_extraction(self):
        data = [
            {'title': 'Ковер', 'price': 2000, 'color': 'green'},
            {'title': 'Диван для отдыха', 'color': 'black'},
            {'color': 'blue'}
        ]
        result = field(data, "title", "price")
        answer = [
            {'title': 'Ковер', 'price': 2000},
            {'title': 'Диван для отдыха'}
        ]
        self.assertEqual(result, answer)


class TestUnique(unittest.TestCase):
    def test_uniqueness(self):
        data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
        result = list(Unique(data))
        self.assertEqual(result, ['a', 'A', 'b', 'B'])
    
    def test_ignore_case(self):
        data = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
        result = list(Unique(data, ignore_case=True))
        self.assertEqual(result, ['a', 'b'])


class TestGenRandom(unittest.TestCase):
    def test_correctness(self):
        n = 100
        mn = 1
        mx = 100
        result = gen_random(n, mn, mx)
        for e in result:
            self.assertTrue(mn <= e <= mx)
        self.assertEqual(len(result), n)
    
    def test_negative_range(self):
        result = gen_random(5, -10, -1)
        for e in result:
            self.assertTrue(e < 0)

unittest.main()