"""
Mixed workload scenario for DocumentDB.

This scenario simulates a balanced workload with various CRUD operations.
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


class MixedWorkloadUser(DocumentDBUser):
    """
    User class for mixed workload testing.
    
    This simulates realistic scenarios with a balance of different
    operation types: Create, Read, Update, Delete.
    """
    
    wait_time = between(0.5, 2)
    
    @task(4)
    def read_document(self):
        """Read operation."""
        start_time = time.time()
        try:
            doc = self.collection.find_one({"type": "mixed_test"})
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read",
                response_time=total_time,
                response_length=len(str(doc)) if doc else 0,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(3)
    def create_document(self):
        """Create operation."""
        start_time = time.time()
        try:
            doc = {
                "type": "mixed_test",
                "timestamp": time.time(),
                "value": random.randint(1, 100),
                "category": random.choice(["A", "B", "C"]),
                "data": f"sample_data_{random.randint(1, 1000)}"
            }
            result = self.collection.insert_one(doc)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="create",
                response_time=total_time,
                response_length=len(str(result.inserted_id)),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="create",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(2)
    def update_document(self):
        """Update operation."""
        start_time = time.time()
        try:
            result = self.collection.update_one(
                {"type": "mixed_test"},
                {"$set": {
                    "updated_at": time.time(),
                    "value": random.randint(1, 100)
                }}
            )
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="update",
                response_time=total_time,
                response_length=result.modified_count,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="update",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(1)
    def delete_document(self):
        """Delete operation."""
        start_time = time.time()
        try:
            # Delete old documents
            cutoff_time = time.time() - 3600  # 1 hour old
            result = self.collection.delete_one(
                {"type": "mixed_test", "timestamp": {"$lt": cutoff_time}}
            )
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="delete",
                response_time=total_time,
                response_length=result.deleted_count,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="delete",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(3)
    def query_with_filter(self):
        """Complex query with filter."""
        start_time = time.time()
        try:
            cursor = self.collection.find({
                "type": "mixed_test",
                "value": {"$gte": 50}
            }).limit(20)
            docs = list(cursor)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="query_filtered",
                response_time=total_time,
                response_length=len(docs),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="query_filtered",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
