#!/usr/bin/env python3
"""
Example script demonstrating the data generator utility.

This script shows how to use the DataGenerator class to create
realistic test data for DocumentDB performance testing.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_generator import DataGenerator
import json


def main():
    """Demonstrate data generation capabilities."""
    
    print("=" * 80)
    print("DocumentDB Test Data Generator - Examples")
    print("=" * 80)
    print()
    
    # Example 1: Generate a user document
    print("1. User Document Example:")
    print("-" * 80)
    user = DataGenerator.generate_user_document()
    print(json.dumps(user, indent=2))
    print()
    
    # Example 2: Generate a product document
    print("2. Product Document Example:")
    print("-" * 80)
    product = DataGenerator.generate_product_document()
    print(json.dumps(product, indent=2))
    print()
    
    # Example 3: Generate a log document
    print("3. Log Document Example:")
    print("-" * 80)
    log = DataGenerator.generate_log_document()
    print(json.dumps(log, indent=2))
    print()
    
    # Example 4: Generate an event document
    print("4. Event Document Example:")
    print("-" * 80)
    event = DataGenerator.generate_event_document()
    print(json.dumps(event, indent=2))
    print()
    
    # Example 5: Generate batch documents
    print("5. Batch Generation Example:")
    print("-" * 80)
    users = DataGenerator.generate_batch_documents('user', count=5)
    print(f"Generated {len(users)} user documents")
    print(f"First user: {json.dumps(users[0], indent=2)}")
    print()
    
    # Example 6: Different document types
    print("6. Batch Generation for Different Types:")
    print("-" * 80)
    products = DataGenerator.generate_batch_documents('product', count=3)
    logs = DataGenerator.generate_batch_documents('log', count=3)
    events = DataGenerator.generate_batch_documents('event', count=3)
    
    print(f"Generated {len(products)} products")
    print(f"Generated {len(logs)} logs")
    print(f"Generated {len(events)} events")
    print()
    
    # Example 7: Using individual helper functions
    print("7. Individual Helper Functions:")
    print("-" * 80)
    print(f"Random string: {DataGenerator.random_string(20)}")
    print(f"Random email: {DataGenerator.random_email()}")
    print(f"Random phone: {DataGenerator.random_phone()}")
    print(f"Random date: {DataGenerator.random_date()}")
    print()
    
    print("=" * 80)
    print("Data generation examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
