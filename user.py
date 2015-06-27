import exception


class User:
    file_name = 'user_info'

    def __init__(self, username, password):
        if type(username) is not str:
            raise exception.IncorrectTypeError('Username must be a string.')
        if type(password) is not str:
            raise exception.IncorrectTypeError('Password must be a string.')
        self.username = username.replace(' ', '-')
        self.password = password.replace(' ', '-')
        if not self.username or not self.password:
            raise exception.EmptyFieldError('Required field left empty.')

    def validate(self):
        try:
            with open(User.file_name) as File:
                for line in File:
                    name, password, newline = line.split(' ')
                    if self.username == name and self.password == password:
                        return True
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
        return False

    def is_name_available(self):
        try:
            with open(User.file_name) as File:
                for line in File:
                    name, password, newline = line.split(' ')
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
        if self.is_name_available():
            try:
                with open(User.file_name, 'a') as File:
                    File.write(self.username + ' ' + self.password + ' \n')
            except IOError as err:
                raise exception.FailedFileOperationError(
                    'Error: "{0}" occurred while trying to write {1}.'.format(
                        str(err), User.file_name
                    )
                )
            return True
        else:
            return False
