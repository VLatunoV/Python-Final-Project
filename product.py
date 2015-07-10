import promotion as promotion_module
import exception


class Product:
    '''
    Функциите в класа приемат вече отворен файл от product manager-а
    '''

    def __init__(
        self, *, name, price, category, tags=[], rating=0, promotion=None,
        rate_count=0
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
        if type(rating) is not int and type(rating) is not float:
            raise exception.IncorrectTypeError('Rating must be int or float.')
        if promotion and type(promotion) is not promotion_module.Promotion:
            raise exception.IncorrectTypeError('This is not a promotion.')
        if type(rate_count) is not int:
            raise exception.IncorrectTypeError('Rate count must be int')
        if not name:
            raise exception.EmptyFieldError('Product name left empty.')
        if price <= 0:
            raise exception.UnallowedValueError('Price must be positive.')
        if not category:
            raise exception.EmptyFieldError('Product category left empty.')
        self.name = name
        self.price = price
        self.category = category
        if type(tags) is str:
            self.tags = [tags]
        else:
            self.tags = tags
        self.rating = rating
        self.promotion = promotion
        self.rate_count = rate_count

    def check_types(self):
        if type(self.name) is not str:
            raise exception.IncorrectTypeError('Product name must be string.')
        if type(self.price) is not int and type(self.price) is not float:
            raise exception.IncorrectTypeError('Price must be int or float.')
        if type(self.category) is not str:
            raise exception.IncorrectTypeError('Category must be string.')
        if not hasattr(self.tags, '__iter__'):
            raise exception.IncorrectTypeError('Tags must be iterable.')
        if any([type(x) is not str for x in self.tags]):
            raise exception.IncorrectTypeError('All tags must be string.')
        if any([not x for x in self.tags]):
            raise exception.UnallowedValueError('Cannot have empty tags.')
        if type(self.rating) is not int \
            and type(self.rating) is not float:
                raise exception.IncorrectTypeError(
                    'Rating must be int or float.'
                )
        if self.promotion \
            and type(self.promotion) is not promotion_module.Promotion:
                raise exception.IncorrectTypeError('This is not a promotion.')
        if not self.name:
            raise exception.EmptyFieldError('Product name left empty.')
        if self.price <= 0:
            raise exception.UnallowedValueError('Price must be positive.')
        if not self.category:
            raise exception.EmptyFieldError('Product category left empty.')
        if type(self.rate_count) is not int:
            raise exception.IncorrectTypeError('Rate count must be int')

    def get_price(self, quantity):
        self.check_types()
        if type(quantity) is not int and type(quantity) is not float:
            raise exception.IncorrectTypeError('Quantity must be a number.')
        if quantity < 1:
            raise exception.UnallowedValueError('Quantity must be positive.')
        if self.promotion:
            return self.promotion.apply(self.price, quantity)
        else:
            return self.price * quantity

    def register(self, File):
        self.check_types()
        File.write('name=' + self.name + '\n')
        File.write('price=' + str(self.price) + '\n')
        File.write('category=' + self.category + '\n')

        File.write('tags=')
        for tag in set(self.tags):
            File.write(tag.replace(' ', '-') + ' ')

        File.write(
            '\n' + 'rating=' + str(self.rating) + ' ' + str(self.rate_count)
        )

        File.write('\n' + 'promotion=')
        if self.promotion:
            File.write(str(self.promotion))
        File.write('\n\n')
        return True

    def read(self, File):
        self.check_types()
        has_data = File.readline()
        if not has_data:
            return False
        self.name = has_data.split('=')[-1][:-1]
        self.price = float(File.readline().split('=')[-1][:-1])
        self.category = File.readline().split('=')[-1][:-1]

        tags = File.readline().split('=')[-1][:-1]
        if tags:
            self.tags = tags.split(' ')[:-1]
        else:
            self.tags = []

        rating = File.readline().split('=')[-1][:-1]
        splet = rating.split(' ')
        self.rating, self.rate_count = float(splet[0]), int(splet[1])
        
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
