# After applying ISP
# Separated interfaces for different database types and messaging services

class MySQLActions:
    def query_mysql(self, sql):
        """Execute MySQL query"""
        pass

    def verify_mysql_result(self, result):
        """Verify MySQL query result"""
        pass


class MongoDBActions:
    def query_mongodb(self, collection, query):
        """Execute MongoDB query"""
        pass

    def aggregate_mongodb(self, collection, pipeline):
        """Execute MongoDB aggregation"""
        pass


class RedisActions:
    def query_redis(self, key):
        """Get Redis value"""
        pass

    def set_redis_value(self, key, value):
        """Set Redis value"""
        pass


class KafkaActions:
    def send_to_kafka(self, topic, message):
        """Send message to Kafka topic"""
        pass

    def read_from_kafka(self, topic):
        """Read message from Kafka topic"""
        pass


class RabbitMQActions:
    def send_to_rabbitmq(self, queue, message):
        """Send message to RabbitMQ queue"""
        pass

    def read_from_rabbitmq(self, queue):
        """Read message from RabbitMQ queue"""
        pass


# Clean implementation for user tests that only need MySQL
class UserDataTest(MySQLActions):
    def test_user_creation(self):
        self.query_mysql("INSERT INTO users (name) VALUES ('John')")
        result = self.query_mysql("SELECT * FROM users WHERE name = 'John'")
        self.verify_mysql_result(result)


# Test that needs both MongoDB and Redis
class CacheTest(MongoDBActions, RedisActions):
    def test_cache_sync(self):
        # Get data from MongoDB
        data = self.query_mongodb("products", {"id": "123"})

        # Verify Redis cache
        cached_data = self.query_redis("product:123")

        # Update cache if needed
        if not cached_data:
            self.set_redis_value("product:123", data)


# Complex test that needs database and messaging
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


# Test class for monitoring that needs multiple messaging systems
class MessageMonitorTest(KafkaActions, RabbitMQActions):
    def test_message_flow(self):
        # Send test message to Kafka
        self.send_to_kafka("test_topic", {"test": "data"})

        # Verify message arrived in RabbitMQ after processing
        processed_message = self.read_from_rabbitmq("processed_queue")
        assert processed_message["status"] == "processed"
