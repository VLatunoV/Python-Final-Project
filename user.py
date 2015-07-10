import exception
import hashlib


class User:
    file_name = 'user_info'

    def __init__(self, username, password, superuser=False):
        if type(username) is not str:
            raise exception.IncorrectTypeError('Username must be a string.')
        if type(password) is not str:
            raise exception.IncorrectTypeError('Password must be a string.')
        if not username or not password:
            raise exception.EmptyFieldError('Required field left empty.')
        self.username = username.replace(' ', '-')
        self.password = password.replace(' ', '-')
        self.superuser = superuser
        if type(superuser) is not bool:
            self.superuser = False

    def check_types(self):
        if type(self.username) is not str:
            raise exception.IncorrectTypeError('Username must be a string.')
        if type(self.password) is not str:
            raise exception.IncorrectTypeError('Password must be a string.')
        if not self.username or not self.password:
            raise exception.EmptyFieldError('Required field left empty.')
        if type(self.superuser) is not bool:
            self.superuser = False

    def validate(self):
        self.check_types()
        try:
            with open(User.file_name) as File:
                hsh = hashlib.sha256()
                hsh.update(bytes(self.password.encode('utf-8')))
                for line in File:
                    name, password, superuser = line.split(' ')[:-1]
                    if self.username == name:
                        if hsh.hexdigest() == password:
                            self.superuser = bool(int(superuser))
                            return True
        except FileNotFoundError:
            try:
                with open(User.file_name, 'w') as f:
                    pass
            except IOError:
                raise exception.FailedFileOperationError(
                    '"{0}" occurred while trying to create {1}.'.format(
                        str(err), User.file_name
                    )
                )
        except IOError as err:
            raise exception.FailedFileOperationError(
                '"{0}" occurred while trying to read {1}.'.format(
                    str(err), User.file_name
                )
            )
        return False

    def is_name_available(self):
        self.check_types()
        try:
            with open(User.file_name) as File:
                for line in File:
                    name = line.split(' ')[0]
                    if self.username == name:
                        return False
        except FileNotFoundError:
            try:
                with open(User.file_name, 'w') as f:
                    pass
            except IOError:
                raise
        except IOError as err:
            raise exception.FailedFileOperationError(
                '"{0}" occurred while trying to read {1}.'.format(
                    str(err), User.file_name
                )
            )
        return True

    def register(self):
        self.check_types()
        if self.is_name_available():
            try:
                with open(User.file_name, 'a') as File:
                    hsh = hashlib.sha256()
                    hsh.update(bytes(self.password.encode('utf-8')))
                    File.write(
                        self.username + ' ' + hsh.hexdigest() + ' ' +
                        str(int(self.superuser)) + ' \n'
                    )
            except IOError as err:
                raise exception.FailedFileOperationError(
                    'Error: "{0}" occurred while trying to write {1}.'.format(
                        str(err), User.file_name
                    )
                )
            return True
        else:
            return False
