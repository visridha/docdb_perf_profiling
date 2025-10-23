"""
Data generation utilities for DocumentDB performance testing.

Provides functions to generate realistic test data for various scenarios.
"""

import random
import string
import time
from datetime import datetime, timedelta


class DataGenerator:
    """Generate test data for DocumentDB performance testing."""
    
    @staticmethod
    def random_string(length=10):
        """Generate a random string of specified length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def random_email():
        """Generate a random email address."""
        username = DataGenerator.random_string(8)
        domain = random.choice(['example.com', 'test.com', 'demo.org'])
        return f"{username}@{domain}"
    
    @staticmethod
    def random_phone():
        """Generate a random phone number."""
        return f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    @staticmethod
    def random_date(start_days_ago=365, end_days_ago=0):
        """Generate a random date within a range."""
        start = datetime.now() - timedelta(days=start_days_ago)
        end = datetime.now() - timedelta(days=end_days_ago)
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + timedelta(days=random_days)
    
    @staticmethod
    def generate_user_document():
        """Generate a sample user document."""
        return {
            "user_id": DataGenerator.random_string(16),
            "username": DataGenerator.random_string(12),
            "email": DataGenerator.random_email(),
            "phone": DataGenerator.random_phone(),
            "created_at": time.time(),
            "profile": {
                "first_name": DataGenerator.random_string(8),
                "last_name": DataGenerator.random_string(10),
                "age": random.randint(18, 80),
                "country": random.choice(['US', 'UK', 'CA', 'AU', 'DE', 'FR'])
            },
            "settings": {
                "notifications": random.choice([True, False]),
                "theme": random.choice(['light', 'dark', 'auto']),
                "language": random.choice(['en', 'es', 'fr', 'de'])
            }
        }
    
    @staticmethod
    def generate_product_document():
        """Generate a sample product document."""
        return {
            "product_id": DataGenerator.random_string(12),
            "name": f"Product {DataGenerator.random_string(8)}",
            "description": f"Description {DataGenerator.random_string(50)}",
            "category": random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports']),
            "price": round(random.uniform(10, 1000), 2),
            "stock": random.randint(0, 1000),
            "tags": [DataGenerator.random_string(6) for _ in range(random.randint(2, 5))],
            "rating": round(random.uniform(1, 5), 1),
            "reviews_count": random.randint(0, 500),
            "created_at": time.time()
        }
    
    @staticmethod
    def generate_log_document():
        """Generate a sample log document."""
        return {
            "log_id": DataGenerator.random_string(20),
            "timestamp": time.time(),
            "level": random.choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
            "service": random.choice(['api', 'worker', 'scheduler', 'frontend']),
            "message": f"Log message {DataGenerator.random_string(30)}",
            "metadata": {
                "request_id": DataGenerator.random_string(16),
                "user_id": DataGenerator.random_string(12),
                "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "duration_ms": random.randint(10, 5000)
            }
        }
    
    @staticmethod
    def generate_event_document():
        """Generate a sample event document."""
        return {
            "event_id": DataGenerator.random_string(16),
            "event_type": random.choice(['click', 'view', 'purchase', 'signup', 'logout']),
            "timestamp": time.time(),
            "user_id": DataGenerator.random_string(12),
            "session_id": DataGenerator.random_string(20),
            "properties": {
                "page": f"/page/{DataGenerator.random_string(8)}",
                "referrer": random.choice(['google', 'facebook', 'direct', 'twitter']),
                "device": random.choice(['mobile', 'desktop', 'tablet']),
                "browser": random.choice(['chrome', 'firefox', 'safari', 'edge'])
            }
        }
    
    @staticmethod
    def generate_batch_documents(doc_type='user', count=100):
        """
        Generate a batch of documents.
        
        Args:
            doc_type: Type of document to generate ('user', 'product', 'log', 'event')
            count: Number of documents to generate
            
        Returns:
            List of generated documents
        """
        generators = {
            'user': DataGenerator.generate_user_document,
            'product': DataGenerator.generate_product_document,
            'log': DataGenerator.generate_log_document,
            'event': DataGenerator.generate_event_document
        }
        
        generator_func = generators.get(doc_type, DataGenerator.generate_user_document)
        return [generator_func() for _ in range(count)]
