"""
Read-heavy workload scenario for DocumentDB.

This scenario simulates a read-intensive workload with 80% read operations
and 20% write operations.
"""

from locust import task, between
import time
from locust import events
import sys
import os

# Add parent directory to path to import from locustfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from locustfile import DocumentDBUser


class ReadHeavyUser(DocumentDBUser):
    """
    User class for read-heavy workload testing.
    
    This simulates scenarios where read operations significantly
    outnumber write operations (e.g., dashboards, analytics).
    """
    
    wait_time = between(0.5, 2)
    
    @task(8)
    def read_single_document(self):
        """Read a single document by ID."""
        start_time = time.time()
        try:
            doc = self.collection.find_one()
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read_single",
                response_time=total_time,
                response_length=len(str(doc)) if doc else 0,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read_single",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(4)
    def scan_documents(self):
        """Scan multiple documents."""
        start_time = time.time()
        try:
            cursor = self.collection.find().limit(50)
            docs = list(cursor)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="scan_documents",
                response_time=total_time,
                response_length=len(docs),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="scan_documents",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(2)
    def write_document(self):
        """Occasional write operation."""
        start_time = time.time()
        try:
            doc = {
                "type": "read_heavy_test",
                "timestamp": time.time(),
                "data": "sample_data"
            }
            result = self.collection.insert_one(doc)
            
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="write_occasional",
                response_time=total_time,
                response_length=len(str(result.inserted_id)),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="write_occasional",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
