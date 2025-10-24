"""
Write-heavy workload scenario for DocumentDB.

This scenario simulates a write-intensive workload with 70% write operations
and 30% read operations.
"""

from locust import task, between
import time
from locust import events
import sys
import os
import random

# Add parent directory to path to import from locustfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from locustfile import DocumentDBUser


class WriteHeavyUser(DocumentDBUser):
    """
    User class for write-heavy workload testing.
    
    This simulates scenarios where write operations significantly
    outnumber read operations (e.g., logging, data ingestion).
    """
    
    wait_time = between(0.1, 1)
    
    @task(7)
    def insert_document(self):
        """Insert a new document."""
        start_time = time.time()
        try:
            doc = {
                "type": "write_heavy_test",
                "timestamp": time.time(),
                "value": random.randint(1, 1000),
                "data": f"data_{random.randint(1, 10000)}"
            }
            result = self.collection.insert_one(doc)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="insert_document",
                response_time=total_time,
                response_length=len(str(result.inserted_id)),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="insert_document",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(2)
    def update_document(self):
        """Update an existing document."""
        start_time = time.time()
        try:
            result = self.collection.update_one(
                {"type": "write_heavy_test"},
                {"$set": {"updated_at": time.time()}}
            )
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="update_document",
                response_time=total_time,
                response_length=result.modified_count,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="update_document",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(3)
    def read_recent_documents(self):
        """Read recently inserted documents."""
        start_time = time.time()
        try:
            cursor = self.collection.find(
                {"type": "write_heavy_test"}
            ).sort("timestamp", -1).limit(10)
            docs = list(cursor)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read_recent",
                response_time=total_time,
                response_length=len(docs),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read_recent",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
