# After applying ISP
# Separated interfaces for different database types and messaging services

# SOLUTION: The Interface Segregation Principle has been applied by breaking down
# the large interface into smaller, more focused interfaces.
# Each class below represents a specific capability that clients can choose to implement.

# Interface for MySQL-specific operations
class MySQLActions:
    def query_mysql(self, sql):
        """Execute MySQL query"""
        pass

    def verify_mysql_result(self, result):
        """Verify MySQL query result"""
        pass


# Interface for MongoDB-specific operations
class MongoDBActions:
    def query_mongodb(self, collection, query):
        """Execute MongoDB query"""
        pass

    def aggregate_mongodb(self, collection, pipeline):
        """Execute MongoDB aggregation"""
        pass


# Interface for Redis-specific operations
class RedisActions:
    def query_redis(self, key):
        """Get Redis value"""
        pass

    def set_redis_value(self, key, value):
        """Set Redis value"""
        pass


# Interface for Kafka messaging operations
class KafkaActions:
    def send_to_kafka(self, topic, message):
        """Send message to Kafka topic"""
        pass

    def read_from_kafka(self, topic):
        """Read message from Kafka topic"""
        pass


# Interface for RabbitMQ messaging operations
class RabbitMQActions:
    def send_to_rabbitmq(self, queue, message):
        """Send message to RabbitMQ queue"""
        pass

    def read_from_rabbitmq(self, queue):
        """Read message from RabbitMQ queue"""
        pass


# BENEFIT: This test class only implements the MySQL interface it needs
# No unnecessary dependencies on other database or messaging systems
class UserDataTest(MySQLActions):
    def test_user_creation(self):
        self.query_mysql("INSERT INTO users (name) VALUES ('John')")
        result = self.query_mysql("SELECT * FROM users WHERE name = 'John'")
        self.verify_mysql_result(result)


# BENEFIT: Multiple inheritance allows composition of only the needed interfaces
# This class needs both MongoDB and Redis capabilities, but nothing else
class CacheTest(MongoDBActions, RedisActions):
    def test_cache_sync(self):
        # Get data from MongoDB
        data = self.query_mongodb("products", {"id": "123"})

        # Verify Redis cache
        cached_data = self.query_redis("product:123")

        # Update cache if needed
        if not cached_data:
            self.set_redis_value("product:123", data)


# BENEFIT: Complex test that needs specific interfaces can mix and match
# precisely what it needs, no more and no less
class OrderProcessingTest(MySQLActions, KafkaActions, RabbitMQActions):
    def test_order_flow(self):
        # Create order in MySQL
        self.query_mysql("INSERT INTO orders (id, status) VALUES (1, 'new')")

        # Send order to Kafka for processing
        self.send_to_kafka("new_orders", {"order_id": 1})

        # Verify order completion message in RabbitMQ
        completion_message = self.read_from_rabbitmq("completed_orders")

        # Verify final status in database
        result = self.query_mysql("SELECT status FROM orders WHERE id = 1")
        self.verify_mysql_result(result)


# BENEFIT: A class that only needs messaging interfaces doesn't need
# to implement any database methods
class MessageMonitorTest(KafkaActions, RabbitMQActions):
    def test_message_flow(self):
        # Send test message to Kafka
        self.send_to_kafka("test_topic", {"test": "data"})

        # Verify message arrived in RabbitMQ after processing
        processed_message = self.read_from_rabbitmq("processed_queue")
        assert processed_message["status"] == "processed"
