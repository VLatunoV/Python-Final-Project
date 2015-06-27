import exception


class Promotion:
    percent_off = 1
    buy_n = 2

    def __init__(self, *, promo_type, value):
        if type(promo_type) is not int:
            raise exception.IncorrectTypeError('Promotion type must be int.')
        if type(value) is not int and type(value) is not float:
            raise exception.IncorrectTypeError(
                'Promotion value must be int or float.')
        self.promo_type = promo_type
        self.value = value

    def apply(self, price, quantity):
        def percent_off():
            if self.value < 0 or self.value >= 100.0:
                raise exception.UnallowedValueError(
                    'Percent off must be between 0 and 100.')
            return price * (1 - self.value / 100.0) * quantity

        def buy_n():
            if int(self.value) < 1:
                raise exception.UnallowedValueError(
                    'n-th free must be more than 1.')
            new_quantity = quantity - quantity // (int(self.value) + 1)
            return price * new_quantity

        easy_access = {
            Promotion.percent_off: percent_off,
            Promotion.buy_n: buy_n
        }
        try:
            return easy_access[self.promo_type]()
        except KeyError:
            raise exception.UnallowedValueError('No such promotion.')

    def __str__(self):
        return str(self.promo_type) + ' ' + str(self.value)

    def receipt_message(self):
        if self.promo_type == Promotion.percent_off:
            return 'Promotion: -{}%'.format(self.value)
        if self.promo_type == Promotion.buy_n:
            return 'Promotion: buy {}, get 1 free'.format(self.value)
