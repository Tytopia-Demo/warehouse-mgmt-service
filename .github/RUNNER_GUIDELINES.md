# GitHub Actions Runner Sizing Guidelines

## Overview
This document provides standardized guidelines for selecting appropriate GitHub Actions runners based on workload requirements. The goal is to optimize performance, cost, and resource utilization across all CI/CD pipelines.

## Runner Types and Sizing

### Small Workloads
**Recommended Runner:** `ubuntu-latest` (2-core, 7GB RAM)
**Use Cases:**
- Linting and code formatting
- Security scanning (static analysis)
- Simple unit tests
- Dependency checks
- Documentation builds

**Timeout:** 10-15 minutes

### Medium Workloads
**Recommended Runner:** `ubuntu-latest` (2-core, 7GB RAM) or `ubuntu-latest-4-cores` (if available)
**Use Cases:**
- Full test suites with moderate coverage
- Building small to medium applications
- Integration tests
- Docker image builds (simple)

**Timeout:** 20-30 minutes

### Large Workloads
**Recommended Runner:** `ubuntu-latest-8-cores` or self-hosted runners
**Use Cases:**
- Complex builds with multiple dependencies
- Extensive test suites
- Multi-platform builds
- Large Docker image builds
- Performance testing

**Timeout:** 45-60 minutes

## Job Categories and Recommended Settings

### Security Scanning Jobs
- **Runner Size:** Small (`ubuntu-latest`)
- **Timeout:** 15 minutes
- **Monitoring Tag:** `workload:security-scan`
- **Notes:** Security scans like Frogbot, Snyk, or Dependabot typically have low resource requirements

### Build Jobs
- **Runner Size:** Medium to Large (depends on codebase)
- **Timeout:** 20-45 minutes
- **Monitoring Tag:** `workload:build`
- **Notes:** Consider caching dependencies to reduce build times

### Test Jobs
- **Runner Size:** Small to Medium (depends on test suite size)
- **Timeout:** 15-30 minutes
- **Monitoring Tag:** `workload:test`
- **Notes:** Use test parallelization for large suites

### Deploy Jobs
- **Runner Size:** Small
- **Timeout:** 20 minutes
- **Monitoring Tag:** `workload:deploy`
- **Notes:** Deployment jobs typically involve API calls and are not resource-intensive

## Best Practices

1. **Always specify timeout-minutes** to prevent jobs from running indefinitely
2. **Use job concurrency controls** to prevent resource contention
3. **Implement caching strategies** for dependencies and build artifacts
4. **Monitor job execution times** regularly to identify optimization opportunities
5. **Use matrix strategies** judiciously to balance parallelization with resource usage
6. **Add cost monitoring labels** to track and optimize spending
7. **Review and adjust** runner sizes quarterly based on actual usage metrics

## Monitoring and Optimization

### Execution Time Tracking
All jobs should output their execution time for monitoring purposes. This is automatically tracked in workflow summaries.

### Cost Monitoring Tags
Use the following labels in your workflows for cost tracking:
- `workload:security-scan`
- `workload:build`
- `workload:test`
- `workload:deploy`
- `workload:utility`

### Performance Metrics to Monitor
- Job execution time
- Queue time
- Success/failure rates
- Resource utilization (CPU, memory)

## Example Configuration

```yaml
jobs:
  security-scan:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    env:
      WORKLOAD_TYPE: security-scan
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run security scan
        # ... scan steps
```

## Migration Strategy

When migrating existing workflows:
1. Audit current runner specifications and job execution times
2. Categorize jobs by workload type
3. Apply appropriate runner sizes and timeouts
4. Monitor performance for 1-2 weeks
5. Adjust as needed based on metrics

## Support and Updates

This document is maintained by the DevOps team. For questions or suggested updates, please open an issue or contact the team directly.

**Last Updated:** 2024
**Version:** 1.0
