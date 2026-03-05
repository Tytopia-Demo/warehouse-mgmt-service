# GitHub Actions Runner Selection Guidelines

## Overview

This document provides guidelines for selecting appropriate GitHub Actions runner types based on workflow resource requirements. Following these guidelines helps optimize costs and improve workflow efficiency.

## Runner Types and Use Cases

### Small Runners: `ubuntu-latest` (2-core)

**Best for:**
- Linting and code formatting (ESLint, Prettier, Black, etc.)
- Security scanning (Frogbot, Snyk, etc.)
- Simple unit tests with fast execution (< 5 minutes)
- Documentation generation
- Dependency updates (Dependabot-like workflows)
- Static code analysis

**Resource Characteristics:**
- CPU: 2 cores
- Memory: 7 GB
- Storage: 14 GB SSD
- Expected Duration: < 10 minutes

**Example workflows:**
- Security scans
- Code quality checks
- Pull request validation

### Medium Runners: `ubuntu-latest-4-core`

**Best for:**
- Integration tests with moderate complexity
- Building medium-sized applications
- Running test suites that require parallel execution
- Docker image builds (simple images)
- Database migration tests

**Resource Characteristics:**
- CPU: 4 cores
- Memory: 16 GB
- Storage: 14 GB SSD
- Expected Duration: 10-30 minutes

**Example workflows:**
- API integration tests
- Multi-service test environments
- Moderate build pipelines

### Large Runners: `ubuntu-latest-8-core` or Custom Runners

**Best for:**
- Full end-to-end test suites
- Complex Docker multi-stage builds
- Performance testing
- Large monorepo builds
- Resource-intensive compilation

**Resource Characteristics:**
- CPU: 8+ cores
- Memory: 32+ GB
- Storage: 14+ GB SSD
- Expected Duration: 30+ minutes

**Example workflows:**
- Complete test matrix runs
- Release builds
- Performance benchmarks

## Workflow Optimization Best Practices

### 1. Set Job Timeouts

Always specify `timeout-minutes` to prevent runaway processes:

```yaml
jobs:
  my-job:
    runs-on: ubuntu-latest
    timeout-minutes: 15  # Adjust based on expected duration
```

**Recommended timeout values:**
- Linting/formatting: 5 minutes
- Security scans: 15 minutes
- Unit tests: 10-15 minutes
- Integration tests: 30 minutes
- Full test suites: 60 minutes

### 2. Add Resource Monitoring

Include resource monitoring steps to track actual usage:

```yaml
steps:
  - name: Log Runner Resources
    run: |
      echo "Runner OS: $RUNNER_OS"
      echo "CPU cores: $(nproc)"
      echo "Memory: $(free -h)"
      echo "Disk: $(df -h)"
```

### 3. Optimize Matrix Strategies

- Only use matrix strategies when testing multiple configurations
- Avoid single-value matrices (use direct values instead)
- Consider fail-fast strategies for quicker feedback

**Bad:**
```yaml
strategy:
  matrix:
    branch: ["master"]  # Single value - unnecessary matrix
```

**Good:**
```yaml
# No matrix needed for single values
env:
  BASE_BRANCH: master
```

**Good (multiple values):**
```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, 3.10, 3.11]
  fail-fast: true  # Stop on first failure
```

### 4. Optimize Job Parallelization

- Split independent jobs to run in parallel
- Use job dependencies (`needs`) appropriately
- Cache dependencies to reduce execution time

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    # Runs independently

  test:
    runs-on: ubuntu-latest
    # Runs independently

  deploy:
    runs-on: ubuntu-latest
    needs: [lint, test]  # Only runs after lint and test succeed
```

### 5. Use Caching Effectively

Cache dependencies to reduce workflow duration:

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

## Resource Categorization

### Current Repository Workflows

| Workflow | Type | Runner | Timeout | Justification |
|----------|------|--------|---------|---------------|
| Frogbot Security Scan | Security | ubuntu-latest | 15 min | Lightweight security scanning with API calls |

## Review and Updates

This document should be reviewed quarterly to ensure runner selections remain optimal based on:
- Historical workflow execution data
- Changes in workflow complexity
- GitHub Actions pricing updates
- New runner types availability

## Contact

For questions or suggestions about runner optimization, please create an issue or contact the DevOps team.
