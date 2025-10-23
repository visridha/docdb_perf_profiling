# DocumentDB Performance Profiling

Performance testing templates and workloads for AWS DocumentDB and MongoDB-compatible databases.

## Overview

This repository provides production-ready performance testing templates for DocumentDB using various performance drivers. Currently includes comprehensive Locust-based templates with more drivers planned for the future.

## Available Templates

### Locust Templates
Comprehensive Locust-based performance testing framework for DocumentDB with multiple workload scenarios.

📁 **Location**: `locust_templates/`

**Features:**
- Multiple pre-built test scenarios (read-heavy, write-heavy, mixed workloads)
- Environment-based configuration
- Realistic data generators
- Distributed testing support
- Comprehensive documentation

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cd locust_templates
cp config/.env.example .env
# Edit .env with your DocumentDB credentials

# Run basic test
locust -f locustfile.py
```

See [locust_templates/README.md](locust_templates/README.md) for detailed documentation.

## Test Scenarios

The following workload scenarios are available:

1. **Basic Workload** - Balanced CRUD operations for general testing
2. **Read-Heavy** - 80% read operations for dashboard/analytics workloads
3. **Write-Heavy** - 70% write operations for logging/ingestion workloads
4. **Mixed Workload** - Realistic CRUD mix for production-like scenarios

## Prerequisites

- Python 3.7+
- DocumentDB cluster or MongoDB-compatible database
- AWS DocumentDB TLS certificate (for AWS deployments)

## Installation

```bash
# Clone the repository
git clone https://github.com/visridha/docdb_perf_profiling.git
cd docdb_perf_profiling

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp locust_templates/config/.env.example locust_templates/.env
```

2. Edit `.env` with your DocumentDB connection details:
```env
DOCDB_HOST=your-cluster.cluster-xxxxx.region.docdb.amazonaws.com
DOCDB_USERNAME=your_username
DOCDB_PASSWORD=your_password
```

3. Download TLS certificate (for AWS DocumentDB):
```bash
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

## Usage Examples

### Run with Web UI
```bash
cd locust_templates
locust -f locustfile.py
# Open http://localhost:8089
```

### Run Headless Mode
```bash
locust -f locustfile.py --headless --users 10 --spawn-rate 1 --run-time 5m
```

### Run Specific Scenario
```bash
# Read-heavy workload
locust -f scenarios/read_heavy.py

# Write-heavy workload
locust -f scenarios/write_heavy.py

# Mixed workload
locust -f scenarios/mixed_workload.py
```

### Distributed Testing
```bash
# Master node
locust -f locustfile.py --master

# Worker nodes (run on multiple machines)
locust -f locustfile.py --worker --master-host=<master-ip>
```

## Project Structure

```
docdb_perf_profiling/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── locust_templates/                  # Locust performance templates
│   ├── README.md                      # Locust documentation
│   ├── locustfile.py                  # Main locust file
│   ├── scenarios/                     # Test scenarios
│   │   ├── read_heavy.py              # Read-intensive workload
│   │   ├── write_heavy.py             # Write-intensive workload
│   │   └── mixed_workload.py          # Mixed CRUD workload
│   ├── utils/                         # Utility modules
│   │   └── data_generator.py          # Test data generation
│   └── config/                        # Configuration files
│       ├── .env.example               # Environment template
│       └── locust.conf                # Locust configuration
└── LICENSE
```

## Customization

### Creating Custom Scenarios

Extend the `DocumentDBUser` class to create custom test scenarios:

```python
from locustfile import DocumentDBUser
from locust import task, between

class MyCustomUser(DocumentDBUser):
    wait_time = between(1, 3)
    
    @task
    def my_custom_test(self):
        # Your custom test logic
        doc = self.collection.find_one({"field": "value"})
```

### Using Data Generators

Generate realistic test data:

```python
from utils.data_generator import DataGenerator

# Generate different types of documents
user = DataGenerator.generate_user_document()
product = DataGenerator.generate_product_document()
batch = DataGenerator.generate_batch_documents('user', count=100)
```

## Monitoring and Metrics

Locust provides multiple ways to monitor and export results:

- **Web UI**: Real-time metrics at http://localhost:8089
- **HTML Reports**: `--html report.html`
- **CSV Export**: `--csv results`

Monitor your DocumentDB instance metrics alongside Locust metrics for comprehensive performance analysis.

## Best Practices

1. **Start with low user counts** and gradually increase load
2. **Monitor DocumentDB metrics** (CPU, memory, connections, IOPS)
3. **Create appropriate indexes** for your query patterns
4. **Use TLS/SSL** in production environments
5. **Test with realistic data** using the provided generators
6. **Run distributed tests** for high-load scenarios
7. **Analyze results** before and after optimizations

## Troubleshooting

### Connection Issues
- Verify DocumentDB endpoint and credentials
- Check security group rules
- Ensure TLS certificate is correctly configured
- Confirm `retryWrites=false` for DocumentDB compatibility

### Performance Issues
- Check DocumentDB instance specifications
- Review query performance and indexes
- Monitor connection pool settings
- Consider scaling DocumentDB resources

## Contributing

Contributions are welcome! Feel free to:
- Add new test scenarios
- Support additional performance drivers
- Improve documentation
- Report issues

## Future Enhancements

- Additional performance drivers (JMeter, K6, etc.)
- More complex test scenarios
- Advanced monitoring integrations
- CI/CD pipeline templates

## License

See [LICENSE](LICENSE) file for details.

## Resources

- [AWS DocumentDB Documentation](https://docs.aws.amazon.com/documentdb/)
- [Locust Documentation](https://docs.locust.io/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

## Support

For issues and questions, please use the GitHub issue tracker.
