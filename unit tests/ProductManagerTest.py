import unittest
import product_manager
import product
import promotion
import exception


class TestProductManager(unittest.TestCase):
    def setUp(self):
        self.pm = product_manager.ProductManager()
        self.pm.file_name = 'product_list_test'

    def test_register(self):
        self.assertTrue(
            self.pm.add_product(
                product.Product(
                    name='prod 1', price=10.00, category='solid',
                    tags=['tag 1', 'tag 2'], rating=7.5
                )
            )
        )
        self.assertTrue(
            self.pm.add_product(
                product.Product(
                    name='prod 2', price=48.26, category='other',
                    tags=['test', 'unit'], rating=5.5
                )
            )
        )
        self.assertTrue(
            self.pm.add_product(
                product.Product(
                    name='prod 3', price=48.26, category='other',
                    tags=['test', 'unit'],
                    promotion=promotion.Promotion(
                        promo_type=0,
                        value=35
                    )
                )
            )
        )
        self.assertFalse(
            self.pm.add_product(
                product.Product(
                    name='prod 1', price=1, category='pass')
            )
        )
        self.assertTrue(self.pm.register_products())

    def test_load(self):
        self.assertTrue(
            self.pm.load_products(file_name='product_list_test_load')
        )
        self.assertTrue(self.pm.register_products())

    def test_exceptions(self):
        self.assertRaises(
            exception.IncorrectTypeError, self.pm.add_product, 'not a product'
        )
        self.assertRaises(
            exception.IncorrectTypeError, self.pm.load_products, file_name=22
        )
        self.assertRaises(
            exception.IncorrectTypeError, self.pm.search,
            123, key='key'
        )
        self.assertRaises(
            exception.EmptyFieldError, self.pm.search,
            '', key='key'
        )
        self.pm.add_product(
            product.Product(
                name='product1', price=48.26, category='other',
                tags=['test', 'unit'],
                promotion=promotion.Promotion(
                    promo_type=0,
                    value=35
                )
            )
        )
        self.assertRaises(
            exception.UnallowedValueError, self.pm.search,
            'string', key='asd'
        )

if __name__ == '__main__':
    unittest.main()
