# Software Entities should be opened for extension, but closed for modification

from enum import Enum


class Products(Enum):
    SHIRT = 1
    TSHIRT = 2
    PANT = 3


class DiscountCalculator:
    def __init__(self, product_type, cost):
        self.product_type = product_type
        self.cost = cost

    def get_discounted_price(self):
        if self.product_type == Products.SHIRT:
            return self.cost - (self.cost * 0.40)
        elif self.product_type == Products.TSHIRT:
            return self.cost - (self.cost * 0.40)
        elif self.product_type == Products.PANT:
            return self.cost - (self.cost * 0.25)


"""
This design breaches the Open Closed principle because this class will need modification if 
a). A new apparel type is to be included and 
b). If the discount amount for any apparel changes
"""

