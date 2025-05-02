# MCP Inspector: Monitoring Guide

## Overview

The MCP Inspector is a powerful diagnostic and monitoring tool designed to provide real-time insights into the performance, health, and operational status of your Master Control Program (MCP) instances. This guide will walk you through setting up and effectively using the MCP Inspector to ensure optimal performance.

## Getting Started

### Installation

```python
# Install the MCP Inspector package
pip install mcp-inspector

# Verify installation
import mcp_inspector
print(mcp_inspector.__version__)
```

### Basic Configuration

Create a configuration file named `inspector_config.yaml` in your project directory:

```yaml
inspector:
  polling_interval: 5  # seconds
  log_level: "INFO"
  dashboard_port: 8080

targets:
  - name: "Primary MCP"
    host: "localhost"
    port: 7000
    auth_token: "your_auth_token"
  
  - name: "Backup MCP"
    host: "backup-server"
    port: 7000
    auth_token: "your_backup_auth_token"
```

## Launching the Inspector

### Command Line Interface

```bash
# Start the MCP Inspector with default configuration
mcp-inspector start

# Start with custom configuration file
mcp-inspector start --config /path/to/inspector_config.yaml

# Start in daemon mode
mcp-inspector start --daemon
```

### Python API

```python
from mcp_inspector import Inspector

# Initialize the inspector
inspector = Inspector(config_path='inspector_config.yaml')

# Start monitoring
inspector.start()

# Later, stop monitoring
inspector.stop()
```

## Monitoring Dashboards

The MCP Inspector provides several web-based dashboards accessible at `http://localhost:8080` (or your configured port):

1. **Overview Dashboard**: Displays the overall health status of all monitored MCPs
2. **Performance Dashboard**: Shows real-time performance metrics
3. **Resource Dashboard**: Monitors resource utilization
4. **Operations Dashboard**: Tracks file operations and their status
5. **Security Dashboard**: Monitors access patterns and potential security issues

## Key Monitoring Features

### 1. Real-time Metrics

The MCP Inspector tracks various performance metrics:

- CPU and memory usage
- Disk I/O operations per second
- Average response time for operations
- Request queue length
- Cache hit/miss ratio
- Number of active sessions

### 2. Health Checks

Automated health checks include:

- Service availability monitoring
- Filesystem integrity verification
- Security policy compliance
- Resource leak detection
- Error rate monitoring

### 3. Alert Configuration

Configure alerts in the `alerts` section of your configuration file:

```yaml
alerts:
  - name: "High CPU Usage"
    metric: "cpu_usage"
    threshold: 85  # percentage
    duration: 60  # seconds
    notification:
      type: "email"
      recipients: ["admin@example.com"]
  
  - name: "Excessive Error Rate"
    metric: "error_rate"
    threshold: 5  # errors per minute
    duration: 120  # seconds
    notification:
      type: "webhook"
      url: "https://your-incident-management-system.com/webhook"
```

## Command Reference

### Checking MCP Status

```python
# Python API
from mcp_inspector import Inspector

inspector = Inspector()

# Get status of all MCPs
all_status = inspector.get_all_status()
print(all_status)

# Get detailed status of a specific MCP
primary_status = inspector.get_status("Primary MCP")
print(primary_status)

# Check if an MCP is healthy
is_healthy = inspector.check_health("Primary MCP")
print(f"Is Primary MCP healthy? {is_healthy}")
```

### CLI Commands

```bash
# Get status summary of all MCPs
mcp-inspector status

# Get detailed status of a specific MCP
mcp-inspector status --target "Primary MCP"

# Check health of all MCPs
mcp-inspector health

# Generate a performance report
mcp-inspector report --from "2024-04-10" --to "2024-04-17"
```

## Troubleshooting with Inspector

The MCP Inspector provides several troubleshooting tools:

### 1. Log Analysis

```python
# Retrieve and analyze logs
from mcp_inspector import LogAnalyzer

analyzer = LogAnalyzer()
issues = analyzer.find_issues(mcp_name="Primary MCP", hours=24)
print(issues)
```

### 2. Performance Profiling

```python
# Start a performance profiling session
from mcp_inspector import Profiler

profiler = Profiler(mcp_name="Primary MCP")
profiler.start()

# ... perform operations to profile ...

# Stop profiling and get results
results = profiler.stop()
profiler.save_report("profile_report.html")
```

### 3. Resource Leak Detection

```python
# Check for resource leaks
from mcp_inspector import LeakDetector

detector = LeakDetector(mcp_name="Primary MCP")
leaks = detector.scan()

if leaks:
    print(f"Found {len(leaks)} potential resource leaks:")
    for leak in leaks:
        print(f"- {leak['resource_type']}: {leak['details']}")
else:
    print("No resource leaks detected.")
```

## Advanced Inspector Features

### 1. Automated Remediation

Configure the inspector to automatically resolve common issues:

```yaml
remediation:
  enabled: true
  actions:
    - issue: "high_memory_usage"
      action: "restart_mcp"
      threshold: 95  # percentage
    
    - issue: "stalled_operations"
      action: "clear_operation_queue"
      threshold: 50  # operations
```

### 2. Custom Plugins

Extend the inspector with custom monitoring plugins:

```python
from mcp_inspector import InspectorPlugin

class CustomMonitor(InspectorPlugin):
    def __init__(self):
        super().__init__(name="custom_monitor")
    
    def collect_metrics(self, mcp):
        # Implement custom metric collection
        return {
            "custom_metric_1": value1,
            "custom_metric_2": value2
        }
    
    def analyze(self, metrics):
        # Analyze collected metrics
        if metrics["custom_metric_1"] > threshold:
            self.report_issue("custom_issue", severity="warning")

# Register the plugin
from mcp_inspector import Inspector
inspector = Inspector()
inspector.register_plugin(CustomMonitor())
```

### 3. Historical Analysis

The MCP Inspector stores historical performance data that can be analyzed for trends:

```python
from mcp_inspector import HistoricalAnalyzer

analyzer = HistoricalAnalyzer()

# Analyze CPU usage trends over the past week
cpu_trends = analyzer.analyze_trend(
    mcp_name="Primary MCP",
    metric="cpu_usage",
    days=7,
    interval="1h"
)

# Plot the results
analyzer.plot_trend(cpu_trends, output_file="cpu_trend.png")
```

## Best Practices

1. **Regular Monitoring**: Check the inspector dashboard daily to identify potential issues before they become critical

2. **Alert Tuning**: Adjust alert thresholds based on your system's normal behavior to reduce false positives

3. **Performance Baselines**: Establish performance baselines during normal operation to better identify abnormal behavior

4. **Periodic Health Checks**: Schedule comprehensive health checks during maintenance windows

5. **Update Inspector**: Keep the MCP Inspector updated to benefit from the latest monitoring capabilities

## Troubleshooting Inspector Issues

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Inspector not connecting to MCP | Authentication failure | Verify auth token in configuration |
| Missing metrics | MCP version incompatibility | Update MCP or Inspector to compatible versions |
| High CPU usage by Inspector | Polling interval too short | Increase polling interval in configuration |
| Dashboard not loading | Port conflict | Change dashboard port in configuration |

## Further Resources

- [MCP Inspector API Documentation](https://mcp-docs.example.com/inspector/api)
- [Monitoring Best Practices Guide](https://mcp-docs.example.com/inspector/best-practices)
- [Custom Plugin Development](https://mcp-docs.example.com/inspector/plugins)
