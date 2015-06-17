import promotion
import exception

class Product:
    def __init__(self, *, name, price, category, tags=None, rating=None,
        promotion=None):
        self.name = name
        self.price = price
        self.category = category
        self.tags = tags
        self.rating = rating
        self.promotion = promotion