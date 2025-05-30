# Automagik Agents Benchmark Report

**Generated:** 2025-05-27 17:17:17 UTC  
**Project Version:** 0.1.4  
**Base URL:** http://localhost:8484  
**Test Mode:** MOCK

## Executive Summary

- **Total Tests:** 6
- **Successful:** 6
- **Failed:** 0  
- **Success Rate:** 100.0%

## Performance Overview

### Detailed Performance Metrics

| Test Name | Status | RPS | Latency | CPU% | RAM(MB) | Error% |
|-----------|--------|-----|---------|------|---------|--------|
| Mock_Infrastructure_Baseline | ✅ PASS | 340.9 | 0.9ms | 0.0% | 0.0 | 0.00% |
| Mock_Medium_Load | ✅ PASS | 876.7 | 0.7ms | 0.0% | 0.0 | 0.00% |
| Mock_High_Concurrency | ✅ PASS | 967.9 | 0.8ms | 0.0% | 0.0 | 0.00% |
| Mock_Extreme_Load | ✅ PASS | 1282.1 | 0.7ms | 0.0% | 0.0 | 0.00% |
| Mock_Stress_Test | ✅ PASS | 1318.4 | 0.7ms | 0.0% | 0.0 | 0.00% |
| Mock_Function_Model_Realistic | ✅ PASS | 452.7 | 140.5ms | 0.0% | 0.0 | 0.00% |

## 🏆 Best Performers

**🚀 Highest Throughput:** Mock_Stress_Test - 1318.4 req/sec

**⚡ Lowest Latency:** Mock_Extreme_Load - 0.7ms

**🖥️ Most CPU Efficient:** Mock_Infrastructure_Baseline - 0.0% CPU

**💾 Most Memory Efficient:** Mock_Infrastructure_Baseline - 0.0 MB peak


## Test Scenarios

### Mock_Infrastructure_Baseline

**Description:** Infrastructure baseline with mock agents  
**Status:** success  
**Duration:** 1.41s  

**Configuration:**
- mode: mock
- mock_type: test
- concurrency: 20
- requests: 100

**Results:**
- Throughput: 340.92 req/sec
- Mean Latency: 0.91 ms
- P95 Latency: 1.08 ms
- Max Latency: 1.9 ms
- CPU Usage: N/A%
- Peak Memory: N/A MB
- Memory Growth: N/A MB
- Error Rate: 0.00%

### Mock_Medium_Load

**Description:** Medium infrastructure load test  
**Status:** success  
**Duration:** 1.50s  

**Configuration:**
- mode: mock
- mock_type: test
- concurrency: 50
- requests: 500

**Results:**
- Throughput: 876.71 req/sec
- Mean Latency: 0.68 ms
- P95 Latency: 0.81 ms
- Max Latency: 1.47 ms
- CPU Usage: N/A%
- Peak Memory: N/A MB
- Memory Growth: N/A MB
- Error Rate: 0.00%

### Mock_High_Concurrency

**Description:** High concurrency infrastructure test  
**Status:** success  
**Duration:** 2.23s  

**Configuration:**
- mode: mock
- mock_type: test
- concurrency: 100
- requests: 1000

**Results:**
- Throughput: 967.87 req/sec
- Mean Latency: 0.77 ms
- P95 Latency: 1.54 ms
- Max Latency: 2.02 ms
- CPU Usage: N/A%
- Peak Memory: N/A MB
- Memory Growth: N/A MB
- Error Rate: 0.00%

### Mock_Extreme_Load

**Description:** Extreme load infrastructure test  
**Status:** success  
**Duration:** 2.61s  

**Configuration:**
- mode: mock
- mock_type: test
- concurrency: 200
- requests: 2000

**Results:**
- Throughput: 1282.09 req/sec
- Mean Latency: 0.65 ms
- P95 Latency: 0.71 ms
- Max Latency: 1.61 ms
- CPU Usage: N/A%
- Peak Memory: N/A MB
- Memory Growth: N/A MB
- Error Rate: 0.00%

### Mock_Stress_Test

**Description:** Maximum stress test for infrastructure  
**Status:** success  
**Duration:** 4.87s  

**Configuration:**
- mode: mock
- mock_type: test
- concurrency: 500
- requests: 5000

**Results:**
- Throughput: 1318.41 req/sec
- Mean Latency: 0.67 ms
- P95 Latency: 0.91 ms
- Max Latency: 26.79 ms
- CPU Usage: N/A%
- Peak Memory: N/A MB
- Memory Growth: N/A MB
- Error Rate: 0.00%

### Mock_Function_Model_Realistic

**Description:** Realistic responses with function model  
**Status:** success  
**Duration:** 3.42s  

**Configuration:**
- mode: mock
- mock_type: function
- concurrency: 100
- requests: 1000

**Results:**
- Throughput: 452.73 req/sec
- Mean Latency: 140.52 ms
- P95 Latency: 206.67 ms
- Max Latency: 258.24 ms
- CPU Usage: N/A%
- Peak Memory: N/A MB
- Memory Growth: N/A MB
- Error Rate: 0.00%


## System Information

- **Test Environment:** http://localhost:8484
- **Project Version:** 0.1.4
- **Test Framework:** Automagik Comprehensive Benchmark Suite
- **Total Test Duration:** 16.03s

## Conclusions


- **Average Throughput:** 873.1 req/sec
- **Average Latency:** 24.0ms
- **System Stability:** 100.0% success rate
- **Performance Status:** Excellent


---
*Report generated by Automagik Benchmark Suite v0.1.4*
