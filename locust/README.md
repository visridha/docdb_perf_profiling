# DocumentDB Locust Performance Templates

This directory contains performance testing templates for DocumentDB using Locust.

## Overview

These templates provide ready-to-use performance test scenarios for DocumentDB, including:

- **Basic CRUD operations** - Simple read/write/query operations
- **Read-heavy workloads** - Optimized for read-intensive applications (80% reads)
- **Write-heavy workloads** - Optimized for write-intensive applications (70% writes)
- **Mixed workloads** - Balanced CRUD operations for realistic scenarios

## Prerequisites

1. Python 3.7 or higher
2. DocumentDB cluster (or MongoDB compatible database)
3. Access credentials and TLS certificate (if using TLS/SSL)

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Download the TLS certificate (if required):
```bash
# For AWS-hosted DocumentDB, use:
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

## Configuration

### Environment Variables

Create a `.env` file based on `config/.env.example`:

```bash
cp config/.env.example .env
```

Edit the `.env` file with your DocumentDB connection details:

```env
DOCDB_HOST=localhost
DOCDB_PORT=10260
DOCDB_USERNAME=your_username
DOCDB_PASSWORD=your_password
DOCDB_DATABASE=testdb
DOCDB_COLLECTION=testcollection
DOCDB_TLS=false
DOCDB_TLS_CA_FILE=/path/to/ca-bundle.pem
```

### Locust Configuration

You can customize Locust settings via command-line arguments or environment variables.

## Usage

### Basic Usage

Run the basic locustfile:

```bash
locust -f locustfile.py
```

Then open http://localhost:8089 in your browser to access the Locust web UI.

### Running Specific Scenarios

#### Read-Heavy Workload
```bash
locust -f scenarios/read_heavy.py
```

#### Write-Heavy Workload
```bash
locust -f scenarios/write_heavy.py
```

#### Mixed Workload
```bash
locust -f scenarios/mixed_workload.py
```

### Headless Mode

Run tests without the web UI:

```bash
locust -f locustfile.py --headless --users 10 --spawn-rate 1 --run-time 5m
```

### Distributed Load Testing

For large-scale testing, you can run Locust in distributed mode:

**Master node:**
```bash
locust -f locustfile.py --master
```

**Worker nodes:**
```bash
locust -f locustfile.py --worker --master-host=<master-ip>
```

## Test Scenarios

### 1. Basic Workload (locustfile.py)

A balanced workload with:
- 50% read operations
- 33% write operations
- 17% query operations

**Use case:** General purpose testing

### 2. Read-Heavy Workload (scenarios/read_heavy.py)

Optimized for read-intensive applications:
- 57% single document reads
- 29% scan operations
- 14% write operations

**Use case:** Dashboards, analytics, reporting systems

### 3. Write-Heavy Workload (scenarios/write_heavy.py)

Optimized for write-intensive applications:
- 58% insert operations
- 17% update operations
- 25% read operations

**Use case:** Logging, data ingestion, event tracking

### 4. Mixed Workload (scenarios/mixed_workload.py)

Realistic CRUD operations:
- 31% read operations
- 23% create operations
- 15% update operations
- 8% delete operations
- 23% filtered queries

**Use case:** General applications with balanced operations

## Data Generation

The `utils/data_generator.py` module provides utilities for generating realistic test data:

```python
from utils.data_generator import DataGenerator

# Generate single documents
user_doc = DataGenerator.generate_user_document()
product_doc = DataGenerator.generate_product_document()

# Generate batch documents
users = DataGenerator.generate_batch_documents('user', count=100)
products = DataGenerator.generate_batch_documents('product', count=50)
```

Available document types:
- `user` - User profile documents
- `product` - E-commerce product documents
- `log` - Application log documents
- `event` - Event tracking documents

## Customization

### Creating Custom Scenarios

To create a custom scenario, extend the `DocumentDBUser` class:

```python
from locustfile import DocumentDBUser
from locust import task, between

class CustomUser(DocumentDBUser):
    wait_time = between(1, 3)
    
    @task(3)
    def my_custom_operation(self):
        # Your custom operation
        pass
```

### Custom Metrics

Use Locust's event system to track custom metrics:

```python
from locust import events
import time

start_time = time.time()
try:
    # Your operation
    result = self.collection.find_one(...)
    
    # Record success
    events.request.fire(
        request_type="DocumentDB",
        name="my_operation",
        response_time=int((time.time() - start_time) * 1000),
        response_length=len(str(result)),
        exception=None,
        context={}
    )
except Exception as e:
    # Record failure
    events.request.fire(
        request_type="DocumentDB",
        name="my_operation",
        response_time=int((time.time() - start_time) * 1000),
        response_length=0,
        exception=e,
        context={}
    )
```

## Best Practices

1. **Start Small**: Begin with a small number of users and gradually increase
2. **Monitor Resources**: Keep an eye on DocumentDB metrics (CPU, memory, connections)
3. **Use Indexes**: Ensure proper indexes are created for query operations
4. **Connection Pooling**: Locust manages connection pooling automatically
5. **TLS Configuration**: Always use TLS in production environments
6. **Realistic Data**: Use the data generator to create realistic test data
7. **Warmup Period**: Allow time for connections to establish before ramping up

## Troubleshooting

### Connection Issues

If you encounter connection errors:

1. Verify DocumentDB endpoint and credentials
2. Check security group rules allow connections from your IP
3. Ensure TLS certificate path is correct
4. Verify `retryWrites=false` for DocumentDB compatibility

### Performance Issues

If tests are slower than expected:

1. Check DocumentDB instance size and scaling
2. Review query performance and indexes
3. Monitor connection count and pool settings
4. Consider distributed testing for higher load

### Common Errors

**Error: SSL handshake failed**
- Download and configure the correct TLS certificate bundle
- Set `DOCDB_TLS_CA_FILE` to the certificate path

**Error: retryWrites is not supported**
- DocumentDB doesn't support retryable writes
- Ensure `DOCDB_RETRY_WRITES=false` in your configuration

## Metrics and Reporting

Locust provides several output formats:

### Web UI
Access real-time metrics at http://localhost:8089

### HTML Report
```bash
locust -f locustfile.py --headless --html report.html
```

### CSV Output
```bash
locust -f locustfile.py --headless --csv results
```

This generates:
- `results_stats.csv` - Request statistics
- `results_stats_history.csv` - Historical data
- `results_failures.csv` - Failure logs

## Additional Resources

- [Locust Documentation](https://docs.locust.io/)
- [DocumentDB GitHub](https://github.com/documentdb/documentdb)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

## Contributing

Feel free to extend these templates with additional scenarios and improvements!
