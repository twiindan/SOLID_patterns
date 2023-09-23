# Software Entities should be opened for extension, but closed for modification

"""
Hence now every sub class would need to
implement the discount part on itself. By doing this we have now removed the previous constraints that required modification to the
base class. Now without modifying the base class we can add more apparels as well as we can change discount amount of an individual
apparel as needed.
"""

from abc import ABC, abstractmethod


class DiscountCalculator(ABC):

    @abstractmethod
    def get_discounted_price(self):
        pass


class DiscountCalculatorShirt(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.10)


class DiscountCalculatorTshirt(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.15)


class DiscountCalculatorPant(DiscountCalculator):
    def __init__(self, cost):
        self.cost = cost

    def get_discounted_price(self):
        return self.cost - (self.cost * 0.25)
