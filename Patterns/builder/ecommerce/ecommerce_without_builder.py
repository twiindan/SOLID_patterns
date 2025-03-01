from dataclasses import dataclass


@dataclass
class Order:
    # Basic Order class using Python's dataclass to automatically generate
    # __init__, __repr__, and other special methods
    id: int  # Unique identifier for the order
    product: str  # Name of the product being ordered
    price: int  # Price per unit of the product
    quantity: int  # Number of units ordered


def test_calculate_final_price():
    # Test function demonstrating direct object creation without a Builder pattern

    # Creating Order objects directly with all parameters specified at once
    # This approach requires knowing the exact order of parameters
    # and providing all parameters at the time of creation
    orders = [Order(1, "Harry Potter", 25, 1),
              Order(2, "Dragon Ball DVD", 50, 1),
              Order(3, "Hammer", 10, 2)]

    # Calculate the total price by summing price * quantity for each order
    total_price = 0
    for order in orders:
        total_price += order.price * order.quantity

    # Verify the calculation is correct: 25*1 + 50*1 + 10*2 = 95
    assert total_price == 95

    # Limitations of this approach:
    # 1. Must provide all parameters at object creation
    # 2. Must remember the correct parameter order
    # 3. No step-by-step construction process
    # 4. Less readable when many parameters are involved
