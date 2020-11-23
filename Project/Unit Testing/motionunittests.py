import unittest
from motion import i
from motion import location

class TestHarness(unittest.TestCase):
    def test_gpio(self):
        self.assertLessEqual(i, 1, "Motion Sensor GPIO Error")
    
    def test_location(self):
        self.assertNotEqual(location, None, "Location not set")


if __name__ == '__main__':
    unittest.main()