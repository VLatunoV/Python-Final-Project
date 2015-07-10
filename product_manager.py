import product as product_module
import exception


class ProductManager:
    def __init__(self):
        self.file_name = 'product_list'
        self.products = []
        self.categories = set()

    def add_product(self, product):
        if type(product) is not product_module.Product:
            raise exception.IncorrectTypeError('This is not a product.')
        for p in self.products:
            if product.name == p.name:
                return False
        self.products.append(product)
        self.categories.add(product.category)
        return True

    def register_products(self):
        try:
            with open(self.file_name, 'w') as File:
                for p in self.products:
                    p.register(File)
        except IOError as err:
            raise exception.FailedFileOperationError(
                '"{0}" occurred while trying to write {1}'.format(
                    str(err), self.file_name
                )
            )
        return True

    def load_products(self, *, file_name=''):
        if type(file_name) is not str:
            raise exception.IncorrectTypeError('File name must be string.')
        if file_name:
            self.file_name = file_name
        try:
            with open(self.file_name) as File:
                kw = {'name': '#', 'price': 1, 'category': '#'}
                while(True):
                    temp = product_module.Product(**kw)
                    if temp.read(File):
                        self.products.append(temp)
                        self.categories.add(temp.category)
                    else:
                        break
        except FileNotFoundError:
            try:
                with open(self.file_name, 'w') as File:
                    pass
            except IOError:
                raise exception.FailedFileOperationError(
                    '"{0}" occurred while trying to create {1}'.format(
                        str(err), self.file_name
                    )
                )
        except IOError as err:
            raise exception.FailedFileOperationError(
                '"{0}" occurred while trying to read {1}'.format(
                    str(err), self.file_name
                )
            )
        return True

    def search(self, keyword, key='name'):
        if type(keyword) is not str:
            raise exception.IncorrectTypeError(
                'Search keyword must be string.'
            )
        if not keyword:
            raise exception.EmptyFieldError('Required keyword left empty.')
        if type(key) is not str:
            raise exception.IncorrectTypeError('Search key must be string.')
        result = []
        try:
            if key == 'tags':
                result = [
                    x for x in self.products if keyword in getattr(x, key)
                ]
            else:
                result = [
                    x for x in self.products if
                    getattr(x, key).find(keyword) != -1
                ]
        except (AttributeError, TypeError):
            raise exception.UnallowedValueError(
                'Cannot search by {}'.format(key)
            )
        else:
            pm = ProductManager()
            pm.products = result
            pm.categories = set([x.category for x in result])
            return pm

    def sort(self, key=lambda x: x.name.lower(), reverse=False):
        try:
            self.products.sort(key=key, reverse=reverse)
        except (AttributeError, ValueError):
            raise exception.UnallowedValueError(
                'Cannot sort by {}'.format(key)
            )
