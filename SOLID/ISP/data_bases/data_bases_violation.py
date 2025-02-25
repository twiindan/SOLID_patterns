# Before applying ISP
# This implementation forces test classes to implement methods for all types of databases
# and messaging services they don't need
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


# Test class forced to implement all methods even though it only needs MySQL
class UserDataTest(DataTestBase):
    def test_user_creation(self):
        self.query_mysql("INSERT INTO users (name) VALUES ('John')")
        # Doesn't need MongoDB, Redis, or messaging methods


# Test class only needs MongoDB but gets everything
class ProductCatalogTest(DataTestBase):
    def test_product_search(self):
        self.query_mongodb("products", {"category": "electronics"})
        # Doesn't need MySQL, Redis, or messaging methods
