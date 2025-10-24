"""
Simple load and query workload for DocumentDB.

This scenario demonstrates a basic workload pattern:
- Load documents (~1KB each) into the database
- Query documents by _id
"""

from locust import task, between
import time
from locust import events
import sys
import os
import random
import string
from bson import ObjectId

# Add parent directory to path to import from locustfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from locustfile import DocumentDBUser


class SimpleLoadQueryUser(DocumentDBUser):
    """
    User class for simple load and query workload.
    
    This workload:
    - Inserts documents of approximately 1KB in size
    - Queries documents by their _id field
    """
    
    wait_time = between(0.5, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inserted_ids = []
    
    def on_start(self):
        """Called when a simulated user starts executing tasks."""
        super().on_start()
        # Pre-populate some documents to query
        self._prepopulate_documents(10)
    
    def _prepopulate_documents(self, count=10):
        """Pre-populate some documents for querying."""
        for _ in range(count):
            doc = self._generate_1kb_document()
            try:
                result = self.collection.insert_one(doc)
                self.inserted_ids.append(result.inserted_id)
            except Exception:
                pass  # Ignore errors during prepopulation
    
    def _generate_1kb_document(self):
        """
        Generate a document of approximately 1KB in size.
        
        Returns a document with various fields totaling ~1KB.
        """
        # Generate random strings to fill up to ~1KB
        # Each character is roughly 1 byte
        # We'll create a document with multiple fields
        
        doc = {
            "type": "load_test_document",
            "timestamp": time.time(),
            "sequence": random.randint(1, 1000000),
            # Main payload field - approximately 800 bytes
            "payload": ''.join(random.choices(string.ascii_letters + string.digits, k=800)),
            # Additional metadata fields
            "metadata": {
                "source": "locust_load_test",
                "version": "1.0",
                "category": random.choice(["A", "B", "C", "D", "E"]),
                "priority": random.randint(1, 5),
                "status": random.choice(["active", "pending", "completed"]),
                "tags": [
                    ''.join(random.choices(string.ascii_lowercase, k=8))
                    for _ in range(5)
                ]
            },
            # Extra data to reach ~1KB
            "data1": ''.join(random.choices(string.ascii_letters, k=50)),
            "data2": ''.join(random.choices(string.ascii_letters, k=50)),
            "data3": ''.join(random.choices(string.ascii_letters, k=50)),
        }
        
        return doc
    
    @task(3)
    def load_document(self):
        """Insert a ~1KB document into the collection."""
        start_time = time.time()
        try:
            doc = self._generate_1kb_document()
            result = self.collection.insert_one(doc)
            
            # Store the ID for later queries
            if len(self.inserted_ids) < 1000:  # Limit the list size
                self.inserted_ids.append(result.inserted_id)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="load_document",
                response_time=total_time,
                response_length=len(str(result.inserted_id)),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="load_document",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(7)
    def query_by_id(self):
        """Query a document by its _id field."""
        start_time = time.time()
        
        # If we don't have any IDs yet, insert one first
        if not self.inserted_ids:
            self._prepopulate_documents(5)
        
        if not self.inserted_ids:
            # Still no IDs, skip this task
            return
        
        try:
            # Pick a random ID from our list
            doc_id = random.choice(self.inserted_ids)
            
            # Query by _id
            doc = self.collection.find_one({"_id": doc_id})
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="query_by_id",
                response_time=total_time,
                response_length=len(str(doc)) if doc else 0,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="query_by_id",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
