import unittest
import product
import os
import exception


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.p = product.Product(
            name='Test name with Intervals', price=14.95, promotion=None,
            tags=['cool', 'tasty', 'tag with interval'], category='taster'
        )
        self.f = open('product_list_test', 'w+')

    def tearDown(self):
        self.f.close()
        os.remove('product_list_test')

    def test_solo_tag(self):
        p = product.Product(
            name='a', price=1, category='a', tags='this tag'
        )
        self.assertEqual(set(['this tag']), set(p.tags))

    def test_load(self):
        self.p.register(self.f)
        self.f.seek(0, 0)
        p2 = product.Product(name='w/e', price=1, category='w/e')
        
        self.assertTrue(p2.read(self.f))
        self.assertEqual(self.p.name, p2.name)
        self.assertEqual(self.p.price, p2.price)
        self.assertEqual(self.p.category, p2.category)
        self.assertEqual(
            {x.replace(' ', '-') for x in self.p.tags},
            set(p2.tags)
        )
        self.assertEqual(self.p.rating, p2.rating)
        self.assertEqual(str(self.p.promotion), str(p2.promotion))
        self.assertFalse(p2.read(self.f))

    def test_exceptions(self):
        self.assertRaises(
            exception.EmptyFieldError, product.Product,
            name='', price=23, category='a'
        )
        self.assertRaises(
            exception.EmptyFieldError, product.Product,
            name='a', price=23, category=''
        )
        self.assertRaises(
            exception.UnallowedValueError, product.Product,
            name='a', price=0, category='a'
        )
        self.assertRaises(
            exception.IncorrectTypeError, product.Product,
            name=3.14, price=1, category='a'
        )
        self.assertRaises(
            exception.IncorrectTypeError, product.Product,
            name='3.14', price=1, category='a', rating='10/10'
        )
        self.assertRaises(
            exception.UnallowedValueError, product.Product,
            name='3.14', price=1, category='a', tags=['e', '']
        )
        self.assertRaises(
            exception.IncorrectTypeError, product.Product,
            name='3.14', price=1, category='a', promotion=['e', '']
        )
        self.assertRaises(
            exception.IncorrectTypeError, product.Product,
            name='3.14', price=1, category='a', tags=99
        )
        self.assertRaises(
            exception.IncorrectTypeError, self.p.get_price, 'not int'
        )
        self.assertRaises(
            exception.UnallowedValueError, self.p.get_price, -1
        )

if __name__ == '__main__':
    unittest.main()
