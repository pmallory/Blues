import unittest
import pixelBasedMusic as pbm
import numpy
from numpy.testing import assert_allclose
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

    def test_rgb2YCbCr(self):
        # assert_allclose checks if all elements of a two sequences are close
        # necessary b/c floating point
        assert_allclose(pbm.rgb2YCbCr((255,0,0)),
                       (76.24499999999999, 84.905000000000001, 255.5))
        assert_allclose(pbm.rgb2YCbCr((255,255,255)),
                       (255.0, 128.0, 128.0))
        assert_allclose(pbm.rgb2YCbCr((50,205,120)),
                       (148.965, 111.69499999999999, 57.385000000000005))


if __name__ == '__main__':
    unittest.main()

