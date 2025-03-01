# Before applying ISP
# This implementation forces test classes to implement methods for all types of databases
# and messaging services they don't need

# PROBLEM: This base class violates the Interface Segregation Principle by forcing clients
# to depend on methods they don't use. It's a "fat interface" that mixes different responsibilities.
class DataTestBase:
    def query_mysql(self, sql):
        """Execute MySQL query"""
        pass

    def query_mongodb(self, collection, query):
        """Execute MongoDB query"""
        pass

    def query_redis(self, key):
        """Get Redis value"""
        pass

    def send_to_kafka(self, topic, message):
        """Send message to Kafka topic"""
        pass

    def read_from_rabbitmq(self, queue):
        """Read message from RabbitMQ queue"""
        pass

    def publish_to_sns(self, topic, message):
        """Publish message to AWS SNS"""
        pass


# VIOLATION: This test class only needs MySQL functionality but is forced to inherit
# all other database and messaging methods it will never use.
# This creates unnecessary dependencies and potential maintenance issues.
class UserDataTest(DataTestBase):
    def test_user_creation(self):
        self.query_mysql("INSERT INTO users (name) VALUES ('John')")
        # Doesn't need MongoDB, Redis, or messaging methods
        # Yet the class still inherits all those unused methods


# VIOLATION: Similarly, this class only needs MongoDB functionality
# but inherits many unnecessary methods, creating a tight coupling
# to functionality it doesn't need.
class ProductCatalogTest(DataTestBase):
    def test_product_search(self):
        self.query_mongodb("products", {"category": "electronics"})
        # Doesn't need MySQL, Redis, or messaging methods
        # This is inefficient and creates dependencies on irrelevant subsystems
