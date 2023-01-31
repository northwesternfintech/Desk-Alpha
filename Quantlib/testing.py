import unittest
from quantlib import QuantLib


class TestAdd(unittest.TestCase):
    def test_variance_std(self):
        ql = QuantLib()
        res1 = ql.variance([1, 2, 3, 4, 5])
        res2 = ql.variance([1, 1, 1, 1, 1, 1])
        res3 = ql.variance([100.5, 200.1, 300.9, 400.8, 500.3])
        self.assertEqual(res1, 2)
        self.assertEqual(res2,0)
        self.assertEqual(res3,20012.0896)

    def test_variance_empty(self):
        ql = QuantLib()
        self.assertEqual(ql.variance([]),0)

    def test_variance_error(self):
        ql = QuantLib()
        self.assertRaises(Exception, ql.variance, [None])
        self.assertRaises(Exception, ql.variance, [1,2,"3"])


if __name__ == '__main__':
    unittest.main()


