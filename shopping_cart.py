import datetime
import exception
import product as product_module


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity=1):
        if type(product) is not product_module.Product:
            raise exception.IncorrectTypeError('This is not a product.')
        if type(quantity) is not int:
            raise exception.IncorrectTypeError('Quantity must be int.')
        if quantity < 1:
            raise exception.UnallowedValueError('Quantity must be positive.')
        try:
            self.items[product] += quantity
        except KeyError:
            self.items[product] = quantity

    def total(self):
        result = 0
        for product, quantity in self.items.items():
            result += product.get_price(quantity)
        return result

    def receipt(self, *, width=50):
        if type(width) is not int:
            raise exception.IncorrectTypeError('Width must be int.')

        # ---------------- Calculate column sizes --------------------------
        if width < 26:  # minimum for date + time
            width = 26
        min_name_width = 8
        min_quantity_width = 5
        min_price_width = 7
        total = self.total()
        price_width = len('{:.2f}'.format(total)) + 2
        if price_width < min_price_width:
            price_width = min_price_width
        quantity_width = 0
        for _, quantity in self.items.items():
            if len(str(quantity)) > quantity_width:
                quantity_width = len(str(quantity))
        quantity_width += 2
        if quantity_width < min_quantity_width:
            quantity_width = min_quantity_width
        name_width = width - (price_width + quantity_width + 3)
        if name_width < min_name_width:
            name_width = min_name_width
        width = name_width + quantity_width + price_width + 3

        # ---------------- Define helping functions ------------------------
        def add_line(*, name_area='-', quantity_area='', price_area=''):
            if name_area == '-':  # spacer line
                return (
                    '+' + '-' * (name_width + quantity_width) + '+' +
                    '-' * price_width + '+' + '\n'
                )
            else:  # actual content
                chunk = len(name_area)
                chunk_size = (name_width - 1)

                # split name area field into chunks to fit in name width
                name_parts = [
                    name_area[i:i + chunk_size]
                    for i in range(0, chunk, chunk_size)
                ]
                result = (
                    '|' + ' ' + name_parts[0].ljust(name_width - 1) +
                    quantity_area.rjust(quantity_width - 1) + ' ' + '|' +
                    price_area.rjust(price_width - 1) + ' ' + '|' + '\n'
                )  # put 1st chunk with quantity and price info
                for part in name_parts[1:]:
                    result += (
                        '|' + ' ' + part.ljust(name_width - 1) +
                        ' ' * quantity_width + '|' +
                        ' ' * price_width + '|' + '\n'
                    )  # leave rest of chunks without
                return result

        def add_footer():  # adds date and time
            result = '|'
            result += (
                'Date: ' + str(datetime.datetime.now())[:-10]
            ).center(width - 2)
            result += '|' + '\n'
            result += '+' + '-' * (width - 2) + '+'
            return result

        # ---------------- Add column names --------------------------------
        result = add_line()
        result += add_line(
            name_area='Product',
            quantity_area='qty',
            price_area='price'
        )
        result += add_line()

        # ---------------- Add products ------------------------------------
        for product, quantity in self.items.items():
            normal_price = product.price * quantity
            result += add_line(
                name_area=product.name,
                quantity_area=str(quantity),
                price_area='{:.2f}'.format(normal_price)
            )
            if product.promotion:
                result += add_line(
                    name_area='   ' + product.promotion.receipt_message(),
                    price_area='{:.2f}'.format(
                        product.get_price(quantity) - normal_price)
                )

        # ---------------------- rest --------------------------------------
        result += add_line()
        result += add_line(
            name_area='Total',
            price_area='{:.2f}'.format(total)
        )
        result += add_line()
        result += add_footer()
        return result
