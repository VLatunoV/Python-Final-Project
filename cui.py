import promotion
import product
import user
import shopping_cart
import product_manager
import exception
import getpass


def get_num(high=0):
    msg = 'Please enter a number'
    if high:
        msg += ' between 1 and {}.'.format(high)
    else:
        msg += '.'
    while(True):
        try:
            number = int(input('> '))
        except ValueError:
            print(msg)
        else:
            if (high and number > high) or number < 1:
                print(msg)
            else:
                break
    return number


class CUI:
    def __init__(self):
        self.user = None
        self.shopping_cart = shopping_cart.ShoppingCart()
        self.product_manager = product_manager.ProductManager()
        try:
            self.product_manager.load_products()
        except exception.GeneralError as err:
            print('Error: ' + str(err))
        self.current_pm = self.product_manager

    def main_loop(self):
        self.login_menu()
        self.shopping_menu()

    def login_menu(self):
        option_list = [('Login', self.login), ('Register', self.register)]
        while(True):
            for index, option in enumerate(option_list):
                print('{}. {}'.format(index + 1, option[0]))
            cmd = get_num(len(option_list))
            try:
                if option_list[cmd - 1][1]():
                    break
            except exception.GeneralError as err:
                    print('Error: ' + str(err))

    def login(self):
        name = input('Username: ')
        password = getpass.getpass()
        self.user = user.User(name, password)
        if self.user.validate():
            return True
        else:
            print('Wrong username or password.')
            return False

    def register(self):
        name = input('Username: ')
        password = getpass.getpass()
        repeat = getpass.getpass('Repeat password: ')
        if password == repeat:
            superuser = input('Superuser? y/n: ')
            if superuser == 'y':
                superuser = True
            else:
                superuser = False
            self.user = user.User(name, password, superuser)
            self.user.register()
            return True
        else:
            print('Passwords do not match.')
            return False

    def shopping_menu(self):
        option_list = [
            ('Buy items', self.buy_items),
            ('Remove items', self.remove_items),
            ('Show shopping cart', self.show_cart),
            ('Show categories', self.show_categories),
            ('Cancel search', self.show_all),
            ('Search', self.search),
            ('Sort', self.sort),
            ('Rate', self.rate),
            ('Checkout', self.checkout)
        ]
        superuser_option_list = [
            ('Add product', self.add_product),
            ('Change product', self.change_product),
            ('Delete product', self.delete_product),
            ('Exit', lambda: True)
        ]
        if self.user.superuser:
            option_list.extend(superuser_option_list)
        while(True):
            for index, option in enumerate(option_list):
                print('{}. {}'.format(index + 1, option[0]))
            cmd = get_num(len(option_list))
            try:
                if option_list[cmd - 1][1]():
                    break
            except exception.GeneralError as err:
                print('Error: ' + str(err))

    def buy_items(self):
        if self.current_pm.products:
            space_count = len(str(len(self.current_pm.products))) + 2
            for index, item in enumerate(self.current_pm.products):
                print(str(index + 1) + '. ' + item.name)
                if item.promotion:
                    if item.promotion.promo_type == 0:
                        print(
                            ' ' * space_count + 'Price: ' + str(item.price) +
                            ' -> ' + str(item.get_price(1))
                        )
                    if item.promotion.promo_type == 1:
                        print(
                            ' ' * space_count + 'Price: ' + str(item.price) +
                            ' -> ' +
                            str(item.get_price(item.promotion.value + 1)) +
                            ' for {} items'.format(item.promotion.value + 1)
                        )
                else:
                    print(' ' * space_count + 'Price: ' + str(item.price))
                if item.rate_count:
                    plural = 'people'
                    if item.rate_count == 1:
                        plural = 'person'
                    print(
                        ' ' * space_count + 'Rating: ' + str(item.rating) +
                        ' ({} {})'.format(item.rate_count, plural)
                    )
                else:
                    print(' ' * space_count + 'Rating: None')
                if item.promotion:
                    print(' ' * space_count + item.promotion.receipt_message())
                print('')
            print('(index)->(quantity)')
            cmd = input()
            try:
                cmd.replace(' ', '')
                seperate = cmd.split(',')
                ind_quant = [tuple(x.split('->')) for x in seperate]
                ind_quant = [(int(tpl[0]), int(tpl[1])) for tpl in ind_quant]
            except (IndexError, ValueError):
                print('Invalid syntax')
                return None
            for index, quantity in ind_quant:
                try:
                    self.shopping_cart.add_item(
                        self.current_pm.products[index - 1], quantity
                    )
                except IndexError:
                    print(
                        'Index must be between 1 and ' +
                        str(len(self.current_pm.products))
                    )
        else:
            print('No products.')

    def show_cart(self):
        if self.shopping_cart.items:
            print(self.shopping_cart.receipt(width=79))
        else:
            print('Shopping cart is empty.')
        input()

    def remove_items(self):
        if self.shopping_cart.items:
            item_list = list(self.shopping_cart.items.keys())
            for index, item in enumerate(item_list):
                print(str(index + 1) + '. ' + item.name)
            cmd = get_num(len(item_list))
            self.shopping_cart.remove_item(item_list[cmd - 1])
        else:
            print('Shopping cart is empty.')

    def search(self):
        print('Search by:')
        print('1. Name')
        print('2. Category')
        print('3. Tag')
        cmd = get_num(3)
        word = input('Search word: ')
        if cmd == 1:
            self.current_pm = self.current_pm.search(word)
        if cmd == 2:
            self.current_pm = self.current_pm.search(word, 'category')
        if cmd == 3:
            self.current_pm = self.current_pm.search(
                word.replace(' ', '-'), 'tags'
            )

    def add_product(self):
        name = input('Name: ')
        try:
            price = float(input('Price: '))
        except ValueError:
            print('Invalid input')
        category = input('Category: ')
        tags = input('Tags: ').split(' ')
        tags = [x for x in tags if x]
        print('Promotion types:')
        print('-1. None')
        for index, desc in enumerate(promotion.Promotion.promo_desc):
            print('{}. {}'.format(index, desc))
        try:
            promo_type = int(input('> '))
        except ValueError:
            print('Invalid input')
        check = None
        if promo_type == -1:
            check = self.product_manager.add_product(
                product.Product(
                    name=name, price=price, category=category, tags=tags
                )
            )
        else:
            try:
                value = float(input('Value: '))
            except ValueError:
                print('Invalid input')
            check = self.product_manager.add_product(
                product.Product(
                    name=name, price=price, category=category, tags=tags,
                    promotion=promotion.Promotion(
                        promo_type=promo_type, value=value
                    )
                )
            )
        if check:
            self.product_manager.register_products()
        else:
            print('Product with the same name already exists')

    def show_categories(self):
        if self.product_manager.categories:
            for cat in self.product_manager.categories:
                print('+-- ' + cat)
        else:
            print('No categories')

    def show_all(self):
        self.current_pm = self.product_manager

    def sort(self):
        print('Sort by:')
        print('1. Name')
        print('2. Price')
        print('3. Rating')
        cmd = get_num(3)
        if cmd == 1:
            self.current_pm.sort()
        if cmd == 2:
            self.current_pm.sort(key=lambda x: x.get_price(1))
        if cmd == 3:
            self.current_pm.sort(key=lambda x: x.rating, reverse=True)

    def checkout(self):
        if self.shopping_cart.items:
            name = 'receipt'
            count = 0
            while(True):
                new_name = name + str(count) + '.txt'
                try:
                    with open(new_name, 'r'):
                        pass
                except FileNotFoundError:
                    try:
                        with open(new_name, 'w') as File:
                            File.write('User: ' + self.user.username + '\n')
                            File.write(self.shopping_cart.receipt())
                    except IOError as err:
                        print('This happened: ' + str(err))
                    break
                except IOError as err:
                    count += 1
                else:
                    count += 1
        return True

    def delete_product(self):
        if self.product_manager.products:
            for index, item in enumerate(self.current_pm.products):
                print(str(index + 1) + '. ' + item.name)
            cmd = get_num(len(self.product_manager.products))
            del self.product_manager.products[cmd - 1]
            self.product_manager.register_products()
        else:
            print('No products')

    def rate(self):
        if self.product_manager.products:
            for index, item in enumerate(self.current_pm.products):
                print(str(index + 1) + '. ' + item.name)
            cmd = get_num(len(self.product_manager.products))
            try:
                new_rate = float(input('Rating: '))
            except ValueError:
                print('Invalid input')
            else:
                if self.product_manager.products[cmd - 1].rating:
                    self.product_manager.products[cmd - 1].rating = (
                        self.product_manager.products[cmd - 1].rate_count *
                        self.product_manager.products[cmd - 1].rating +
                        new_rate
                    ) / (self.product_manager.products[cmd - 1].rate_count + 1)
                else:
                    self.product_manager.products[cmd - 1].rating = new_rate
                self.product_manager.products[cmd - 1].rate_count += 1
                self.product_manager.register_products()
        else:
            print('No products to rate')

    def change_product(self):
        if self.product_manager.products:
            for index, item in enumerate(self.current_pm.products):
                print(str(index + 1) + '. ' + item.name)
            cmd = get_num(len(self.product_manager.products))
            print('What attribute')
            print('1. Name')
            print('2. Price')
            print('3. Category')
            print('4. Tags')
            print('5. Promotion')
            num = get_num(5)
            if num == 1:
                new_val = input('New name: ')
                if new_val in [x.name for x in self.product_manager.products]:
                    print('Product with the same name already exists')
                else:
                    self.product_manager.products[cmd - 1].name = new_val
            if num == 2:
                try:
                    new_val = float(input('New price: '))
                except ValueError:
                    print('Invalid input')
                self.product_manager.products[cmd - 1].price = new_val
            if num == 3:
                new_val = input('New category: ')
                self.product_manager.products[cmd - 1].category = new_val
            if num == 4:
                new_val = input('New tags: ')
                tag_list = new_val.replace(' ', '-').split(',')
                self.product_manager.products[cmd - 1].tags = tag_list
            if num == 5:
                try:
                    for index, promo_type in \
                            enumerate(promotion.Promotion.promo_desc):
                        print('{}. {}'.format(index, promo_type))
                    promo_type = int(input('New promotion type: '))
                    promo_value = float(input('New promotion value: '))
                except ValueError:
                    print('Invalid input')
                self.product_manager.products[cmd - 1].promotion = \
                    promotion.Promotion(
                        promo_type=promo_type, value=promo_value
                    )
            try:
                self.product_manager.products[cmd - 1].check_types()
            except exception.GeneralError as err:
                print(err)
            else:
                self.product_manager.register_products()
        else:
            print('No products to change')
