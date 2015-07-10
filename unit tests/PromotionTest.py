import unittest
import promotion
import exception


class TestPromotion(unittest.TestCase):
    def setUp(self):
        self.p1 = promotion.Promotion(
            promo_type=0,
            value=0
        )
        self.p2 = promotion.Promotion(
            promo_type=1,
            value=0
        )

    def test_apply(self):
        self.p1.value = 15
        self.assertEqual(self.p1.apply(50.00, 1), 50.00 * (1 - 0.15))

        self.p2.value = 4
        self.assertEqual(self.p2.apply(20, 4), self.p2.apply(20, 5))
        self.assertEqual(self.p2.apply(20, 10), 20 * 8)
        self.assertEqual(self.p2.apply(20, 12), 20 * 10)

    def test_exceptions(self):
        self.p1.value = 150
        self.assertRaises(exception.UnallowedValueError, self.p1.apply, 10, 5)

        self.p2.promo_type = -20
        self.assertRaises(exception.UnallowedValueError, self.p2.apply, 10, 10)

        self.assertRaises(
            exception.IncorrectTypeError, promotion.Promotion,
            promo_type='not int', value=10
        )
        self.assertRaises(
            exception.IncorrectTypeError, promotion.Promotion,
            promo_type=1, value=(10.32,)
        )
        self.assertRaises(
            exception.UnallowedValueError, promotion.Promotion,
            promo_type=4, value=10.32
        )

    def test_to_string(self):
        self.p1.value = 55.004
        self.assertEqual(str(self.p1), '0 55.004')

if __name__ == '__main__':
    unittest.main()
