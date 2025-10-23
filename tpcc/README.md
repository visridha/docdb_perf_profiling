# TPC-C Benchmarks for DocumentDB

This directory contains TPC-C benchmark templates for DocumentDB performance testing.

## Overview

TPC-C is a popular OLTP (Online Transaction Processing) benchmark that simulates a wholesale supplier managing orders. This directory will contain:

- TPC-C schema adapted for DocumentDB
- Transaction implementations
- Setup and execution scripts
- Performance analysis tools

## Getting Started

Documentation and templates will be added here for running TPC-C benchmarks against DocumentDB.

## Transactions

TPC-C includes five transaction types:

1. **New Order**: Enter a new order from a customer
2. **Payment**: Update customer balance and record payment
3. **Order Status**: Retrieve status of customer's most recent order
4. **Delivery**: Process a batch of orders for delivery
5. **Stock Level**: Determine stock levels for items in recent orders

## Schema

The TPC-C schema will be adapted for DocumentDB's document model, including:

- Warehouse documents
- District documents
- Customer documents
- Order documents
- Item documents

## Resources

- [TPC-C Specification](http://www.tpc.org/tpcc/)
- [TPC-C Benchmarking Guide](http://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp)
