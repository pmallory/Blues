import unittest
import pixelBasedMusic as pbm
from math import sqrt

class Test(unittest.TestCase):

    def test_euclidean_distance(self):
        self.assertEqual(pbm.euclidean_distance((1,1,1),(1,1,1)),0)
        self.assertEqual(pbm.euclidean_distance((1,0,0),(0,0,0)),1)
        self.assertAlmostEqual(pbm.euclidean_distance((1,1,1),(0,0,0)),sqrt(3))

    def test_closest_color(self):
        self.assertEqual(pbm.closest_color((250,0,0)), 'red')
        self.assertEqual(pbm.closest_color((250,150,0)), 'orange')
        self.assertEqual(pbm.closest_color((250,240,0)), 'yellow')
        self.assertEqual(pbm.closest_color((25,250,10)), 'green')
        self.assertEqual(pbm.closest_color((100,230,200)), 'aqua')
        self.assertEqual(pbm.closest_color((0,0,200)), 'blue')
        self.assertEqual(pbm.closest_color((120,0,250)), 'violet')

    def test_spiral(self):
        self.assertSequenceEqual(list(pbm.spiral(3,3)), [(1, 1), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0)])
        self.assertSequenceEqual(list(pbm.spiral(3, 5)), [(1, 2), (2, 2), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1), (1, 1), (2, 1), (2, 4), (1, 4), (0, 4), (0, 0), (1, 0), (2, 0)])

if __name__ == '__main__':
    unittest.main()

