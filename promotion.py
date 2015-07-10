import exception


class Promotion:
    promo_desc = [
        'Percent off', 'N-th free'
    ]

    def __init__(self, *, promo_type, value):
        if type(promo_type) is not int:
            raise exception.IncorrectTypeError('Promotion type must be int.')
        if type(value) is not int and type(value) is not float:
            raise exception.IncorrectTypeError(
                'Promotion value must be int or float.'
            )
        if promo_type >= len(Promotion.promo_desc) or promo_type < -1:
            raise exception.UnallowedValueError(
                'Promotion type must be between 0 and {}'.format(
                    len(Promotion.promo_desc) - 1
                )
            )
        self.promo_type = promo_type
        self.value = value
        if self.promo_type == 1:
            self.value = int(self.value)

    def check_types(self):
        if type(self.promo_type) is not int:
            raise exception.IncorrectTypeError('Promotion type must be int.')
        if type(self.value) is not int and type(self.value) is not float:
            raise exception.IncorrectTypeError(
                'Promotion value must be int or float.'
            )
        if self.promo_type >= len(Promotion.promo_desc) \
            or self.promo_type < -1:
                raise exception.UnallowedValueError(
                    'Promotion type must be between 0 and {}'.format(
                        len(Promotion.promo_desc) - 1
                    )
                )
        if self.promo_type == 1:
            self.value = int(self.value)

    def apply(self, price, quantity):
        self.check_types()
        def percent_off():
            if self.value < 0 or self.value >= 100.0:
                raise exception.UnallowedValueError(
                    'Percent off must be between 0 and 100.'
                )
            return price * (1 - self.value / 100.0) * quantity

        def buy_n():
            if int(self.value) < 1:
                raise exception.UnallowedValueError(
                    'N-th free must be more than 1.'
                )
            new_quantity = quantity - quantity // (int(self.value) + 1)
            return price * new_quantity

        easy_access = [percent_off, buy_n]
        try:
            return easy_access[self.promo_type]()
        except IndexError:
            raise exception.UnallowedValueError('No such promotion.')

    def __str__(self):
        self.check_types()
        return str(self.promo_type) + ' ' + str(self.value)

    def receipt_message(self):
        self.check_types()
        msg = [
            'Promotion: -{}%'.format(self.value),
            'Promotion: buy {}, get 1 free'.format(self.value)
        ]
        return msg[self.promo_type]
