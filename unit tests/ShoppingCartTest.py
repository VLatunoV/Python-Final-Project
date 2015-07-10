import unittest
import shopping_cart
import product
import promotion
import exception


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.sc = shopping_cart.ShoppingCart()

    def test_total_price(self):
        self.sc.add_item(
            product.Product(
                name='Rubbery product #1', price=200, category='w/e',
                promotion=promotion.Promotion(
                    promo_type=0,
                    value=50
                )
            )
        ) # worth 50.00
        self.sc.add_item(
            product.Product(
                name='Hat of many shades', price=10, category='w/e',
                promotion=promotion.Promotion(
                    promo_type=1,
                    value=3
                )
            ), 8
        ) # worth 60.00
        self.sc.add_item(
            product.Product(
                name='Necessarily long product name (for testing purposes)',
                price=12.50, category='w/e'
            ), 3
        ) # worth 37.50
        self.assertEqual(self.sc.total(), 197.5)
        # f = open('receipt', 'w')
        # f.write(self.sc.receipt(width=77))
        # f.close()

    def test_exceptions(self):
        p = product.Product(name='some', price=5.00, category='q')
        self.assertRaises(
            exception.IncorrectTypeError, self.sc.add_item, 'not a product',
        )
        self.assertRaises(
            exception.IncorrectTypeError, self.sc.add_item, p, 'not int'
        )
        self.assertRaises(
            exception.UnallowedValueError, self.sc.add_item, p, -50
        )
        self.assertRaises(
            exception.IncorrectTypeError, self.sc.receipt, width=(1, 2, 3)
        )

if __name__ == '__main__':
    unittest.main()
