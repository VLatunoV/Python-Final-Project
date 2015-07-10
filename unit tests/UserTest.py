import unittest
import user
import exception
import os


class TestUser(unittest.TestCase):
    def setUp(self):
        self.u = user.User('user name', 'pass 123')
        user.User.file_name = 'user_info_test'

    def test_correct_init(self):
        self.assertEqual(self.u.username, 'user-name')
        self.assertEqual(self.u.password, 'pass-123')

    def test_exceptions(self):
        self.assertRaises(exception.EmptyFieldError, user.User, '', '')
        self.assertRaises(exception.EmptyFieldError, user.User, '', 'a')
        self.assertRaises(exception.EmptyFieldError, user.User, 's', '')

        self.assertRaises(exception.IncorrectTypeError, user.User, 34, 'str')
        self.assertRaises(exception.IncorrectTypeError, user.User, 'a', (1, 2))

    def test_validate(self):
        self.assertTrue(self.u.register())
        self.assertTrue(self.u.validate())
        self.assertFalse(self.u.is_name_available())
        self.assertEqual(self.u.superuser, False)

        os.remove(user.User.file_name)

    def test_file_doesnt_exist(self):
        user.User.file_name = 'pqowieurytlaksjdhfg019283745'

        self.assertTrue(self.u.is_name_available())
        self.assertFalse(self.u.validate())
        self.assertTrue(self.u.register())
        self.assertTrue(self.u.validate())

        os.remove(user.User.file_name)

if __name__ == '__main__':
    unittest.main()
