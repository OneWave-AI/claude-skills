# Swarm Architecture

The commander coordinates the full lifecycle across six phases.

```
Commander
 |
 |-- Phase 1: Intake & Inventory
 |    |-- Count total items
 |    |-- Sample items for schema detection
 |    |-- Estimate token budget per item
 |
 |-- Phase 2: Swarm Design
 |    |-- Calculate optimal batch size
 |    |-- Determine number of swarm agents
 |    |-- Define result schema
 |
 |-- Phase 3: Deploy Swarm (parallel)
 |    |-- Agent S1: items 1-50      ---\
 |    |-- Agent S2: items 51-100     ---|
 |    |-- Agent S3: items 101-150    ---|-- All run in parallel
 |    |-- Agent S4: items 151-200    ---|
 |    |-- ...                       ---/
 |
 |-- Phase 4: Collect & Aggregate
 |    |-- Gather all agent results
 |    |-- Merge into unified output
 |    |-- Identify failures
 |
 |-- Phase 5: Recovery (if needed)
 |    |-- Retry failed items
 |    |-- Fill gaps
 |
 |-- Phase 6: Deliver
 |    |-- Write final output
 |    |-- Generate summary report
```
