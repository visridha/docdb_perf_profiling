# Quick Start Guide

Get started with DocumentDB performance testing in 5 minutes!

## Prerequisites

- Python 3.7+
- DocumentDB cluster or MongoDB-compatible database
- Basic understanding of load testing concepts

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Connection

Create a `.env` file in the `locust` directory:

```bash
cd locust
cp config/.env.example .env
```

Edit `.env` with your DocumentDB credentials:

```env
DOCDB_HOST=localhost
DOCDB_PORT=10260
DOCDB_USERNAME=admin
DOCDB_PASSWORD=your_password
DOCDB_DATABASE=testdb
DOCDB_COLLECTION=testcollection
```

## Step 3: Configure TLS (Optional)

If your DocumentDB instance requires TLS/SSL:

Update `.env` with the certificate path:
```env
DOCDB_TLS=true
DOCDB_TLS_CA_FILE=/path/to/your-ca-bundle.pem
```

## Step 4: Run Your First Test

### Option A: Using the Quick Start Script (Recommended)

```bash
cd locust
./run_test.sh
```

### Option B: Using Locust Directly

```bash
cd locust
locust -f locustfile.py
```

Then open http://localhost:8089 in your browser.

## Step 5: Configure and Start Test

In the Locust web UI:

1. **Number of users**: Start with 10
2. **Spawn rate**: 1 user per second
3. **Host**: Leave empty (configured via environment)
4. Click **Start swarming**

## Trying Different Scenarios

### Read-Heavy Workload
Perfect for testing dashboards and analytics:
```bash
locust -f scenarios/read_heavy.py
```

### Write-Heavy Workload
Perfect for testing logging and data ingestion:
```bash
locust -f scenarios/write_heavy.py
```

### Mixed Workload
Perfect for realistic application testing:
```bash
locust -f scenarios/mixed_workload.py
```

## Running in Headless Mode

For automated testing without the web UI:

```bash
./run_test.sh --headless --users 50 --spawn-rate 5 --run-time 10m
```

Or with Locust directly:

```bash
locust -f locustfile.py --headless \
    --users 50 \
    --spawn-rate 5 \
    --run-time 10m \
    --html report.html
```

## Understanding Results

After the test completes, you'll see:

- **Request/s**: Operations per second
- **Response times**: p50, p95, p99 percentiles
- **Failure rate**: Percentage of failed operations
- **HTML Report**: Detailed statistics (when using `--html`)

## Common Issues

### Connection Timeout
- Check security group rules
- Verify DocumentDB endpoint
- Ensure TLS certificate is valid

### Authentication Error
- Verify username and password
- Check database permissions

### Slow Performance
- Start with fewer users
- Check DocumentDB instance size
- Review query patterns and indexes

## Next Steps

1. Review the [full documentation](locust/README.md)
2. Customize scenarios for your use case
3. Use the data generator for realistic test data
4. Set up distributed testing for higher loads
5. Monitor DocumentDB metrics alongside Locust results

## Example Test Run

Here's what a successful test looks like:

```
[2025-10-23 10:00:00,000] INFO/locust.main: Starting Locust 2.15.0
[2025-10-23 10:00:00,100] INFO/locust.main: Starting web interface at http://0.0.0.0:8089
[2025-10-23 10:00:30,000] INFO/locust.runners: Spawning 10 users at rate 1.00 users/s
[2025-10-23 10:00:40,000] INFO/locust.runners: All users spawned

Type     Name                      # reqs   # fails  Avg    Min    Max  Median  req/s
------------------------------------------------------------------------
DocumentDB read_document            500      0      45     12     156    42     5.2
DocumentDB write_document           300      0      67     23     234    58     3.1
DocumentDB query_documents          150      0      89     34     312    78     1.6
------------------------------------------------------------------------
Aggregated                          950      0      58     12     312    52    10.0
```

## Tips for Success

1. **Start small**: Begin with 1-5 users to verify connectivity
2. **Ramp gradually**: Increase load slowly to identify breaking points
3. **Monitor both sides**: Watch both Locust and DocumentDB metrics
4. **Test realistic scenarios**: Use workloads that match your application
5. **Run multiple tests**: Vary parameters to understand performance characteristics

Happy testing! 🚀
