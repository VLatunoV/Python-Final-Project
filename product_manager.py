import product
#import exception

class ProductManager:
    def __init__(self):
        file_name = 'product_list'
        self.products = []
        self.categories = set()
        self.__ID_NEXT = 0

    def add_product(self, product):
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
            return False
        return True

    def load_products(self, *, file_name=''):
        if file_name:
            self.file_name = file_name
        try:
            with open(self.file_name) as File:
                self.__ID_NEXT = int(File.readline()[:-1])
                kw = {'name': '#', 'ID': 0, 'price': 0, 'category': '#'}
                while(True):
                    temp = product.Product(**kw)
                    if temp.read(File):
                        self.products.append(temp)
                        self.categories.add(temp.category)
                    else:
                        break
        except IOError:
            return False
        return True
