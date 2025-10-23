# YCSB Benchmarks for DocumentDB

This directory contains Yahoo! Cloud Serving Benchmark (YCSB) templates for DocumentDB performance testing.

## Overview

YCSB is a popular framework for evaluating the performance of NoSQL databases. This directory will contain:

- YCSB workload configurations for DocumentDB
- Custom workload definitions
- Setup and execution scripts
- Result analysis tools

## Getting Started

Documentation and templates will be added here for running YCSB benchmarks against DocumentDB.

## Workloads

Standard YCSB workloads that will be included:

- **Workload A**: Update heavy (50% reads, 50% updates)
- **Workload B**: Read mostly (95% reads, 5% updates)
- **Workload C**: Read only (100% reads)
- **Workload D**: Read latest (95% reads, 5% inserts)
- **Workload E**: Scan heavy (95% scans, 5% inserts)
- **Workload F**: Read-modify-write (50% reads, 50% read-modify-writes)

## Resources

- [YCSB GitHub](https://github.com/brianfrankcooper/YCSB)
- [YCSB Documentation](https://github.com/brianfrankcooper/YCSB/wiki)
