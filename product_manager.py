import product as product_module
import exception


class ProductManager:
    def __init__(self):
        file_name = 'product_list'
        self.products = []
        self.categories = set()
        self.__ID_NEXT = 0

    def add_product(self, product):
        if type(product) is not product_module.Product:
            raise exception.IncorrectTypeError('This is not a product.')
        for p in self.products:
            if product.name == p.name:
                return False
        product.ID = self.__ID_NEXT
        self.__ID_NEXT += 1
        self.products.append(product)
        self.categories.add(product.category)
        return True

    def register_products(self):
        try:
            with open(self.file_name, 'w+') as File:
                File.write(str(self.__ID_NEXT) + '\n')
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
                self.__ID_NEXT = int(File.readline()[:-1])
                kw = {'name': '#', 'ID': 1, 'price': 1, 'category': '#'}
                while(True):
                    temp = product_module.Product(**kw)
                    if temp.read(File):
                        self.products.append(temp)
                        self.categories.add(temp.category)
                    else:
                        break
        except FileNotFoundError:
            raise exception.FileMissingError(
                'File "{0}" is missing.'.format(self.file_name)
            )
        except IOError as err:
            raise exception.FailedFileOperationError(
                '"{0}" occurred while trying to read {1}'.format(
                    str(err), self.file_name
                )
            )
        return True
