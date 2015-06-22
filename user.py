import exception

class User:
    file_name = 'user_info'
    def __init__(self, username, password):
        self.username = username.replace(' ', '-')
        self.password = password.replace(' ', '-')
        if not self.username or not self.password:
            raise exception.EmptyStringError

    def validate(self):
        try:
            with open(User.file_name) as File:
                for line in File:
                    name, password, newline = line.split(' ')
                    if self.username == name and self.password == password:
                        return True
        except FileNotFoundError:
            f = open(User.file_name, 'w')
            f.close()
        except IOError:
            pass
        return False

    def is_name_available(self):
        try:
            with open(User.file_name) as File:
                for line in File:
                    name, password, newline = line.split(' ')
                    if self.username == name:
                        return False
        except FileNotFoundError:
            f = open(User.file_name, 'w')
            f.close()
        except IOError:
            pass
        return True

    def register(self):
        if self.is_name_available():
            try:
                with open(User.file_name, 'a') as File:
                    File.write(self.username + ' ' + self.password + ' \n')
            except IOError:
                return False
            return True
        else:
            return False
