import unittest
from .practise_1_15 import Drone


class TestDrone(unittest.TestCase):
    def setUp(self):
        self.drone = Drone()

    def test_takeoff(self):
        # высокий уровень заряда
        self.drone.battery_level = 50
        result = self.drone.takeoff()
        self.assertTrue(self.drone.is_flying)
        self.assertEqual(result, "Дрон взлетел")

        # низкий уровень заряда
        self.drone.battery_level = 10
        result = self.drone.takeoff()
        self.assertFalse(self.drone.is_flying)
        self.assertEqual(result, "Низкий заряд батареи для взлета")

    def test_land_not_flying(self):
        self.drone.is_flying = False
        result = self.drone.land()
        self.assertFalse(self.drone.is_flying)
        self.assertEqual(result, "Дрон уже на земле")

    def test_land_flying(self):
        self.drone.is_flying = True
        result = self.drone.land()
        self.assertFalse(self.drone.is_flying)
        self.assertEqual(result, "Дрон приземлился")


if __name__ == "__main__":
    unittest.main()



