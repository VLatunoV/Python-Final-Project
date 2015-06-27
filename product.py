import promotion as promotion_module
import exception


class Product:
    '''
    Функциите в класа приемат вече отворен файл от product manager-а
    '''

    def __init__(
        self, *, name, price, category, ID=-1, tags=[], rating=None,
        promotion=None
    ):
        if type(name) is not str:
            raise exception.IncorrectTypeError('Product name must be string.')
        if type(price) is not int and type(price) is not float:
            raise exception.IncorrectTypeError('Price must be int or float.')
        if type(category) is not str:
            raise exception.IncorrectTypeError('Category must be string.')
        if not hasattr(tags, '__iter__'):
            raise exception.IncorrectTypeError('Tags must be iterable.')
        if any([type(x) is not str for x in tags]):
            raise exception.IncorrectTypeError('All tags must be string.')
        if any([not x for x in tags]):
            raise exception.UnallowedValueError('Cannot have empty tags.')
        if rating and type(rating) is not int and type(rating) is not float:
            raise exception.IncorrectTypeError('Rating must be int or float.')
        if promotion and type(promotion) is not promotion_module.Promotion:
            raise exception.IncorrectTypeError('This is not a promotion.')
        if not name:
            raise exception.EmptyFieldError('Product name left empty.')
        if price <= 0:
            raise exception.UnallowedValueError('Price must be positive.')
        if not category:
            raise exception.EmptyFieldError('Product category left empty.')
        self.name = name
        self.price = price
        self.category = category
        self.ID = ID
        if type(tags) is str:
            self.tags = [tags]
        else:
            self.tags = tags
        self.rating = rating
        self.promotion = promotion

    def get_price(self, quantity):
        if type(quantity) is not int:
            raise exception.IncorrectTypeError('Quantity must be int.')
        if quantity < 1:
            raise exception.UnallowedValueError('Quantity must be position.')
        if self.promotion:
            return self.promotion.apply(self.price, quantity)
        else:
            return self.price * quantity

    def check_exists(self, File):
        position = File.tell()
        result = False
        File.seek(0, 0)
        for line in File:
            parts = line.split('=')
            if parts[0] == 'name' and parts[-1][:-1] == self.name:
                result = True
                break
            if parts[0] == 'ID' and parts[-1][:-1] == self.ID:
                result = True
                break
        File.seek(position, 0)
        return result

    def register(self, File):
        if self.check_exists(File):
            return False
        File.write('name=' + self.name + '\n')
        File.write('price=' + str(self.price) + '\n')
        File.write('category=' + self.category + '\n')
        File.write('ID=' + str(self.ID) + '\n')

        File.write('tags=')
        for tag in set(self.tags):
            File.write(tag.replace(' ', '-') + ' ')

        File.write('\n' + 'rating=')
        if self.rating:
            File.write(str(self.rating))

        File.write('\n' + 'promotion=')
        if self.promotion:
            File.write(str(self.promotion))
        File.write('\n\n')
        return True

    def read(self, File):
        has_data = File.readline()
        if not has_data:
            return False
        self.name = has_data.split('=')[-1][:-1]
        self.price = float(File.readline().split('=')[-1][:-1])
        self.category = File.readline().split('=')[-1][:-1]
        self.ID = int(File.readline().split('=')[-1][:-1])
        tags = File.readline().split('=')[-1][:-1]
        if tags:
            self.tags = tags.split(' ')[:-1]
        else:
            self.tags = []
        rating = File.readline().split('=')[-1][:-1]
        if rating:
            self.rating = float(rating)
        else:
            self.rating = None
        promo = File.readline().split('=')[-1][:-1]
        if promo:
            promo_type, value = promo.split(' ')
            self.promotion = promotion_module.Promotion(
                promo_type=int(promo_type), value=float(value)
            )
        else:
            self.promotion = None
        File.readline()  # empty line after each product
        return True
