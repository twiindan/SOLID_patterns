from dataclasses import dataclass


@dataclass
class Order:
    id: int
    product: str
    price: int
    quantity: int


class OrderBuilder:
    def __init__(self):
        self._order = Order(1, "Harry Potter", 25, 1)

    def with_price(self, price: int):
        self._order.price = price
        return self

    def with_quantity(self, quantity: int):
        self._order.quantity = quantity
        return self

    def with_product(self, product: str):
        self._order.product = product
        return self

    def build(self):
        return self._order


def test_calculate_final_price_with_different_prices():

    orders = [OrderBuilder().with_price(25).build(),
              OrderBuilder().with_price(50).build(),
              OrderBuilder().with_price(10).build()]

    total_price = 0
    for order in orders:
        total_price += order.price * order.quantity

    assert total_price == 85


def test_calculate_final_price_with_different_quantities():

    orders = [OrderBuilder().with_quantity(1).build(),
              OrderBuilder().with_quantity(2).build(),
              OrderBuilder().with_quantity(3).build()]

    total_price = 0
    for order in orders:
        total_price += order.price * order.quantity

    assert total_price == 150
