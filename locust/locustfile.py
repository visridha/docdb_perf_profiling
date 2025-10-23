"""
Main Locust file for DocumentDB performance testing.

This file provides a basic template for load testing DocumentDB using Locust.
It can be extended with custom scenarios and configurations.
"""

from locust import User, task, between, events
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import os
import time
import logging

logger = logging.getLogger(__name__)


class DocumentDBClient:
    """
    A wrapper client for DocumentDB operations to be used with Locust.
    """
    
    def __init__(self, host, port=10260, username=None, password=None, 
                 database="test", tls=True, tls_ca_file=None, 
                 retry_writes=False, read_preference="primary"):
        """
        Initialize DocumentDB client.
        
        Args:
            host: DocumentDB cluster endpoint
            port: Port number (default: 10260)
            username: Database username
            password: Database password
            database: Database name to use
            tls: Enable TLS/SSL (default: True for DocumentDB)
            tls_ca_file: Path to CA certificate bundle
            retry_writes: Enable retry writes (default: False for DocumentDB)
            read_preference: Read preference mode
        """
        connection_string = self._build_connection_string(
            host, port, username, password, tls, tls_ca_file, retry_writes, read_preference
        )
        
        self.client = MongoClient(connection_string)
        self.db = self.client[database]
        
    def _build_connection_string(self, host, port, username, password, tls, 
                                  tls_ca_file, retry_writes, read_preference):
        """Build MongoDB connection string."""
        auth_part = f"{username}:{password}@" if username and password else ""
        connection_string = f"mongodb://{auth_part}{host}:{port}/"
        
        params = []
        if tls:
            params.append("tls=true")
        if tls_ca_file:
            params.append(f"tlsCAFile={tls_ca_file}")
        if not retry_writes:
            params.append("retryWrites=false")
        if read_preference:
            params.append(f"readPreference={read_preference}")
            
        if params:
            connection_string += "?" + "&".join(params)
            
        return connection_string
    
    def get_collection(self, collection_name):
        """Get a collection from the database."""
        return self.db[collection_name]
    
    def close(self):
        """Close the database connection."""
        if self.client:
            self.client.close()


class DocumentDBUser(User):
    """
    Base Locust User class for DocumentDB testing.
    
    This class provides basic configuration and setup for DocumentDB connections.
    Extend this class to create specific test scenarios.
    """
    
    abstract = True  # This prevents Locust from using this class directly
    wait_time = between(1, 3)  # Wait time between tasks
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get configuration from environment variables
        self.host = os.getenv("DOCDB_HOST", "localhost")
        self.port = int(os.getenv("DOCDB_PORT", "10260"))
        self.username = os.getenv("DOCDB_USERNAME")
        self.password = os.getenv("DOCDB_PASSWORD")
        self.database = os.getenv("DOCDB_DATABASE", "testdb")
        self.collection_name = os.getenv("DOCDB_COLLECTION", "testcollection")
        
        # TLS configuration
        self.tls_enabled = os.getenv("DOCDB_TLS", "true").lower() == "true"
        self.tls_ca_file = os.getenv("DOCDB_TLS_CA_FILE")
        
        # Connection settings
        self.retry_writes = os.getenv("DOCDB_RETRY_WRITES", "false").lower() == "true"
        self.read_preference = os.getenv("DOCDB_READ_PREFERENCE", "primary")
        
    def on_start(self):
        """Called when a simulated user starts executing tasks."""
        try:
            self.client = DocumentDBClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database,
                tls=self.tls_enabled,
                tls_ca_file=self.tls_ca_file,
                retry_writes=self.retry_writes,
                read_preference=self.read_preference
            )
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Connected to DocumentDB: {self.host}")
        except Exception as e:
            logger.error(f"Failed to connect to DocumentDB: {e}")
            raise
    
    def on_stop(self):
        """Called when a simulated user stops executing tasks."""
        if hasattr(self, 'client'):
            self.client.close()
            logger.info("Closed DocumentDB connection")


class BasicDocumentDBUser(DocumentDBUser):
    """
    Basic DocumentDB user with simple read and write operations.
    
    This provides a starting template for common CRUD operations.
    """
    
    @task(3)
    def read_document(self):
        """Read a random document from the collection."""
        start_time = time.time()
        try:
            # Read one document
            doc = self.collection.find_one()
            
            # Fire success event
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read_document",
                response_time=total_time,
                response_length=len(str(doc)) if doc else 0,
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="read_document",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(2)
    def write_document(self):
        """Write a document to the collection."""
        start_time = time.time()
        try:
            # Insert a test document
            doc = {
                "test_field": f"test_value_{time.time()}",
                "timestamp": time.time(),
                "user_id": self.context.get("user_id", "unknown") if hasattr(self, 'context') else "unknown"
            }
            result = self.collection.insert_one(doc)
            
            # Fire success event
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="write_document",
                response_time=total_time,
                response_length=len(str(result.inserted_id)),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="write_document",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
    
    @task(1)
    def query_documents(self):
        """Query documents with a filter."""
        start_time = time.time()
        try:
            # Query with a simple filter
            cursor = self.collection.find({"timestamp": {"$gt": time.time() - 3600}}).limit(10)
            docs = list(cursor)
            
            # Fire success event
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="query_documents",
                response_time=total_time,
                response_length=len(docs),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="DocumentDB",
                name="query_documents",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
