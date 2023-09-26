from abc import ABC, abstractmethod


class Burger(ABC):
    @abstractmethod
    def cook(self):
        pass


class BeefBurgers(Burger):
    def cook(self):
        print('Beef Burgers')


class ChickenBurger(Burger):
    def cook(self):
        print('Chicken Burger')


class FishBurger(Burger):
    def cook(self):
        print('Fish Burger')


# Factory Object
class BurgerStoreFactory(object):
    @staticmethod
    def get_burguer(name):
        if name == 'Beef':
            return BeefBurgers()
        elif name == 'Chicken':
            return ChickenBurger()
        elif name == 'Fish':
            return FishBurger()


# Client Code
if __name__ == '__main__':
    # Create burger "Beef burger"
    b = BurgerStoreFactory()
    burger = b.get_burguer('Beef')
    burger.cook()

    # Create burger "Chicken burger"
    burger = b.get_burguer('Chicken')
    burger.cook()

    # Create burger "Fish burger"
    burger = b.get_burguer('Fish')
    burger.cook()
