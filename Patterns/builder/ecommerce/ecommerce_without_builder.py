from dataclasses import dataclass


@dataclass
class Order:
    id: int
    product: str
    price: int
    quantity: int


def test_calculate_final_price():
    orders = [Order(1, "Harry Potter", 25, 1),
              Order(2, "Dragon Ball DVD", 50, 1),
              Order(3, "Hammer", 10, 2)]

    total_price = 0
    for order in orders:
        total_price += order.price * order.quantity

    assert total_price == 95

