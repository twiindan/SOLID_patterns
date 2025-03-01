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
    def get_burger(name):
        if name == 'Beef':
            return BeefBurgers()
        elif name == 'Chicken':
            return ChickenBurger()
        elif name == 'Fish':
            return FishBurger()


# Client Code
if __name__ == '__main__':
    # Create burger "Beef burger"
    burger_factory = BurgerStoreFactory()
    burger = burger_factory.get_burger('Beef')
    burger.cook()

    # Create burger "Chicken burger"
    burger = burger_factory.get_burger('Chicken')
    burger.cook()

    # Create burger "Fish burger"
    burger = burger_factory.get_burger('Fish')
    burger.cook()
