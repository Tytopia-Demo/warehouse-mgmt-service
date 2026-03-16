# GitHub Actions Workflow Optimization

This directory contains optimized GitHub Actions workflows and related documentation for the warehouse-mgmt-service repository.

## Overview

The workflows in this repository have been optimized for:
- **Right-sized runners** based on actual workload requirements
- **Appropriate timeout configurations** to prevent runaway jobs
- **Execution time tracking** for performance monitoring
- **Cost monitoring tags** for resource utilization tracking
- **Standardized configurations** following best practices

## Directory Structure

```
.github/
├── workflows/
│   ├── frogbot.yml                    # Optimized security scanning workflow
│   ├── reusable-security-scan.yml     # Reusable security scan template
│   ├── reusable-build.yml             # Reusable build template
│   ├── reusable-test.yml              # Reusable test template
│   └── example-optimized-ci.yml       # Example CI pipeline with all optimizations
├── scripts/
│   └── analyze-workflow-performance.py # Performance analysis script
├── runner-config.yml                  # Runner configuration matrix
├── RUNNER_GUIDELINES.md              # Comprehensive runner sizing guidelines
└── README.md                         # This file
```

## Key Optimizations Applied

### 1. Runner Right-Sizing

Each workflow job is assigned a runner size appropriate to its workload:

- **Small runners** (`ubuntu-latest`): Security scans, linting, simple tests
- **Medium runners** (`ubuntu-latest`): Builds, integration tests
- **Large runners** (self-hosted or larger): Complex builds, extensive test suites

### 2. Timeout Configuration

All jobs now have explicit timeout values to prevent:
- Jobs running indefinitely due to hangs or deadlocks
- Excessive resource consumption
- Delayed feedback on failures

### 3. Execution Time Tracking

All optimized workflows include:
- Start time recording
- End time recording
- Duration calculation
- Metrics output to workflow summaries

### 4. Cost Monitoring Tags

Workflows use environment variables for cost tracking:
- `WORKLOAD_TYPE`: Category of work (security-scan, build, test, deploy, utility)
- `RUNNER_SIZE`: Size of runner used (small, medium, large)

### 5. Standardized Configurations

- Consistent naming conventions
- Reusable workflow templates
- Documented best practices
- Matrix configurations for different scenarios

## Using Reusable Workflows

The repository includes reusable workflow templates that can be called from other workflows:

### Example: Using the Security Scan Template

```yaml
jobs:
  security-scan:
    uses: ./.github/workflows/reusable-security-scan.yml
    with:
      runner-size: small
      timeout-minutes: 15
      scan-branch: main
    secrets:
      jf-url: ${{ secrets.JF_URL }}
      jf-access-token: ${{ secrets.JF_ACCESS_TOKEN }}
      git-token: ${{ secrets.GITHUB_TOKEN }}
```

### Example: Using the Build Template

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      runner-size: medium
      timeout-minutes: 30
      python-version: '3.9'
```

## Performance Analysis

Use the included analysis script to monitor workflow performance:

```bash
# Analyze all workflows from the last 30 days
python .github/scripts/analyze-workflow-performance.py

# Analyze a specific workflow
python .github/scripts/analyze-workflow-performance.py --workflow "Frogbot Security Scan"

# Analyze a custom time period
python .github/scripts/analyze-workflow-performance.py --days 7
```

**Requirements:**
- GitHub CLI (`gh`) installed and authenticated
- Python 3.6+ with PyYAML library

## Runner Selection Guidelines

Refer to [RUNNER_GUIDELINES.md](./RUNNER_GUIDELINES.md) for detailed information on:
- Runner types and specifications
- Workload categorization
- Timeout recommendations
- Best practices
- Migration strategies

## Configuration Reference

The [runner-config.yml](./runner-config.yml) file contains the standardized configuration matrix defining:
- Runner types (small, medium, large)
- Default timeouts by runner type
- Workload categories and recommendations
- Cost monitoring tags
- Optimization features

## Monitoring and Metrics

### What Gets Tracked

Each optimized workflow tracks:
- Job execution time (start to finish)
- Runner size used
- Workload type
- Job status (success/failure)
- Timeout limit

### Viewing Metrics

Metrics are available in:
1. **Workflow Summary**: View in the Actions tab after each run
2. **Job Logs**: Execution time printed in the final step
3. **GitHub API**: Queryable via API for historical analysis

## Best Practices for New Workflows

When creating new workflows:

1. **Start with a reusable template** if available
2. **Categorize the workload** (security-scan, build, test, deploy, utility)
3. **Select the appropriate runner size** based on guidelines
4. **Set a reasonable timeout** (2-3x expected execution time)
5. **Add execution time tracking** steps
6. **Include cost monitoring tags** in environment variables
7. **Use caching** for dependencies when possible
8. **Document any custom configurations**

## Migration Checklist

For existing workflows:

- [ ] Audit current runner specifications
- [ ] Analyze historical execution times
- [ ] Categorize workload type
- [ ] Apply appropriate runner size
- [ ] Add timeout-minutes configuration
- [ ] Add execution time tracking steps
- [ ] Add cost monitoring environment variables
- [ ] Test the updated workflow
- [ ] Monitor performance for 1-2 weeks
- [ ] Adjust as needed

## Cost Optimization Impact

Expected benefits from these optimizations:

- **Reduced wasted resources** through appropriate runner sizing
- **Faster feedback loops** from optimized job configurations
- **Better visibility** into resource consumption
- **Prevented runaway jobs** through timeout configurations
- **Data-driven decisions** via execution time tracking

## Support and Maintenance

### Reporting Issues

If you encounter issues with the optimized workflows:
1. Check the workflow logs for error messages
2. Verify timeout values are appropriate
3. Review the runner guidelines
4. Open an issue with relevant details

### Updates and Improvements

This optimization framework is designed to evolve:
- Review performance metrics quarterly
- Adjust runner sizes based on actual usage
- Update timeout values as needed
- Incorporate feedback from the team

### Contributing

When contributing workflow changes:
1. Follow the established patterns
2. Update documentation as needed
3. Test changes thoroughly
4. Include performance metrics in PR description

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Runner Specifications](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)

## Version History

- **v1.0** (2024): Initial runner optimization implementation
  - Right-sized runners for all workflows
  - Timeout configurations added
  - Execution time tracking implemented
  - Cost monitoring tags applied
  - Reusable templates created
  - Documentation completed
