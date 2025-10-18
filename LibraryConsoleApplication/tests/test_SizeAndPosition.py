import unittest
from Presentation.ConsoleUI.Components.SizeAndPosition import SizeAndPosition

class TestSizeAndPosition(unittest.TestCase):
    def test_init_and_properties(self):
        s = SizeAndPosition(left=10, top=20, height=30, width=40)
        self.assertEqual(s.left, 10)
        self.assertEqual(s.top, 20)
        self.assertEqual(s.width, 40)
        self.assertEqual(s.height, 30)
        self.assertEqual(s.right, 50)
        self.assertEqual(s.bottom, 50)

    def test_setters_validation(self):
        s = SizeAndPosition(0, 0, 10, 10)
        with self.assertRaises(ValueError):
            s.width = 0
        with self.assertRaises(ValueError):
            s.height = -5
        with self.assertRaises(ValueError):
            s.top = -1
        with self.assertRaises(ValueError):
            s.left = -2

    def test_right_and_bottom_setters(self):
        s = SizeAndPosition(10, 10, 20, 30)
        s.right = 50
        self.assertEqual(s.width, 40)
        s.bottom = 70
        self.assertEqual(s.height, 60)

    def test_eq(self):
        a = SizeAndPosition(5, 5, 10, 10)
        b = SizeAndPosition(5, 5, 10, 10)
        c = SizeAndPosition(0, 0, 10, 10)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
