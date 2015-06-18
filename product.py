import promotion
#import exception

class Product:
    def __init__(self, *, name, price, category, ID, tags=[], rating=None,
        promotion=None):
        self.name = name
        self.price = price
        self.category = category
        self.ID = ID
        self.tags = tags
        self.rating = rating
        self.promotion = promotion

    def check_exists(self, File):
        position = File.tell()
        result = False
        File.seek(0, 0)
        for line in File:
            parts = line.split('=')
            if parts[0] == 'name' and parts[-1][:-1] == self.name:
                result = True
            if parts[0] == 'ID' and parts[-1][:-1] == self.ID:
                result = True
        File.seek(position, 0)
        return result

    def register(self, File):
        if self.check_exists(File):
            return False
        #if type(self.name) is not str:
        #    raise exception.IncorrectTypeError
        File.write('name=' + self.name + '\n')

        #if type(self.price) is not int and type(self.price) is not float:
        #    raise exception.IncorrectTypeError
        File.write('price=' + str(self.price) + '\n')

        #if type(self.category)
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
            self.promotion = promotion.Promotion(
                promo_type=int(promo_type), value=float(value)
            )
        else:
            self.promotion = None
        File.readline()
        return True