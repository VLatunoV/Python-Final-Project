import exception

class Promotion:
    '''
    Class for product promotions
    Promotion types:
        percent off
        buy n, get 1 free
    '''
    percent_off = 1
    buy_n = 2
    def __init__(self, *, promo_type, value):
        self.promo_type = promo_type
        self.value = value

    def apply(self, price, quantity):
        def percent_off():
            if self.value < 0 or self.value >= 100.0:
                raise exception.UnallowedValueError
            return price * (1 - self.value / 100.0) * quantity
        def buy_n():
            if int(self.value) < 1:
                raise exception.UnallowedValueError
            new_quantity = quantity - quantity // (int(self.value) + 1)
            return price * new_quantity

        easy_access = {
            Promotion.percent_off: percent_off,
            Promotion.buy_n: buy_n
        }
        try:
            return easy_access[self.promo_type]()
        except KeyError:
            raise exception.UnallowedTypeError

    def __str__(self):
        return str(self.promo_type) + ' ' + str(self.value)