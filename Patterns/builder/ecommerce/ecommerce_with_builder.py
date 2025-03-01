from dataclasses import dataclass


@dataclass
class Order:
    # Basic Order class, same structure as in the non-builder example
    id: int  # Unique identifier for the order
    product: str  # Name of the product being ordered
    price: int  # Price per unit of the product
    quantity: int  # Number of units ordered


class OrderBuilder:
    # Builder pattern implementation for creating Order objects
    # This pattern allows step-by-step construction of complex objects

    def __init__(self):
        # Initialize with default values for a new Order
        # The builder starts with a base order that can be customized
        self._order = Order(1, "Harry Potter", 25, 1)

    def with_price(self, price: int):
        # Set the price for the order being built
        self._order.price = price
        # Return self to allow method chaining
        return self

    def with_quantity(self, quantity: int):
        # Set the quantity for the order being built
        self._order.quantity = quantity
        # Return self to allow method chaining
        return self

    def with_product(self, product: str):
        # Set the product name for the order being built
        self._order.product = product
        # Return self to allow method chaining
        return self

    def build(self):
        # Return the final constructed Order object
        return self._order


def test_calculate_final_price_with_different_prices():
    # Test function demonstrating builder pattern with different prices

    # Creating orders using the builder pattern
    # Note how we only specify the price, keeping other values as default
    # The fluent interface (method chaining) makes the code more readable
    orders = [OrderBuilder().with_price(25).build(),
              OrderBuilder().with_price(50).build(),
              OrderBuilder().with_price(10).build()]

    # Calculate the total price as before
    total_price = 0
    for order in orders:
        total_price += order.price * order.quantity

    # Verify the calculation: 25*1 + 50*1 + 10*1 = 85
    assert total_price == 85


def test_calculate_final_price_with_different_quantities():
    # Test function demonstrating builder pattern with different quantities

    # Creating orders using the builder pattern
    # Here we only modify the quantity, keeping default values for other properties
    orders = [OrderBuilder().with_quantity(1).build(),
              OrderBuilder().with_quantity(2).build(),
              OrderBuilder().with_quantity(3).build()]

    # Calculate the total price
    total_price = 0
    for order in orders:
        total_price += order.price * order.quantity

    # Verify the calculation: 25*1 + 25*2 + 25*3 = 150
    assert total_price == 150

    # Advantages of the Builder pattern:
    # 1. Step-by-step construction of complex objects
    # 2. Only specify the parameters you want to change
    # 3. Method names clearly indicate what each parameter means
    # 4. Fluent interface with method chaining improves readability
    # 5. Can create different configurations with a single builder class
