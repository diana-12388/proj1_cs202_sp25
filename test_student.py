import unittest
from proj1 import (GlobeRect, Region, RegionCondition, emissions_per_capita, area, emissions_per_square_km, densest)
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        # NY setup
        self.ny_rect = GlobeRect(40.5, 41, -74.3, -73.7)
        self.ny_reg = Region(self.ny_rect, "New York", "other")
        self.ny = RegionCondition(self.ny_reg, 2025, 20000000, 50000000.0)
        
        # Tokyo setup
        self.tk_rect = GlobeRect(35.5, 36, 139.5, 140)
        self.tk_reg = Region(self.tk_rect, "Tokyo", "other")
        self.tokyo = RegionCondition(self.tk_reg, 2025, 14000000, 40000000.0)

    def test_emissions_per_capita(self):
        # 50,000,000 / 20,000,000 = 2.5
        self.assertAlmostEqual(emissions_per_capita(self.ny), 2.5, places=4)

    def test_area(self):
        self.assertTrue(area(self.ny.region.rect) > 0)

    def test_densest(self):
        # Tokyo is smaller in area than NY but has high pop, usually denser
        actual = densest([self.ny, self.tokyo])
        self.assertEqual(actual, "Tokyo")

if __name__ == '__main__':
    unittest.main()
