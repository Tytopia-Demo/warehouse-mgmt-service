#!/usr/bin/env python3
"""
Workflow Performance Analysis Script

This script analyzes GitHub Actions workflow runs to provide insights on:
- Execution times by job and workload type
- Runner utilization patterns
- Cost optimization opportunities
- Timeout configuration recommendations

Usage:
    python analyze-workflow-performance.py [--days DAYS] [--workflow WORKFLOW_NAME]

Requirements:
    - GitHub CLI (gh) installed and authenticated
    - PyYAML library (pip install pyyaml)
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta

def run_gh_command(command):
    """Execute a GitHub CLI command and return the output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}", file=sys.stderr)
        return None

def get_workflow_runs(workflow_name=None, days=30):
    """Fetch recent workflow runs"""
    date_limit = (datetime.now() - timedelta(days=days)).isoformat()

    cmd = f"gh run list --limit 100 --json name,status,conclusion,createdAt,updatedAt,workflowName"
    if workflow_name:
        cmd += f" --workflow '{workflow_name}'"

    output = run_gh_command(cmd)
    if not output:
        return []

    try:
        runs = json.loads(output)
        return [r for r in runs if r['createdAt'] >= date_limit]
    except json.JSONDecodeError:
        print("Error parsing workflow runs", file=sys.stderr)
        return []

def analyze_runs(runs):
    """Analyze workflow runs and generate statistics"""
    stats = {
        'total_runs': len(runs),
        'by_workflow': defaultdict(lambda: {'count': 0, 'success': 0, 'failure': 0, 'total_duration': 0}),
        'by_status': defaultdict(int),
        'by_conclusion': defaultdict(int)
    }

    for run in runs:
        workflow_name = run['workflowName']
        status = run['status']
        conclusion = run.get('conclusion', 'unknown')

        stats['by_workflow'][workflow_name]['count'] += 1
        stats['by_status'][status] += 1
        stats['by_conclusion'][conclusion] += 1

        if conclusion == 'success':
            stats['by_workflow'][workflow_name]['success'] += 1
        elif conclusion in ['failure', 'cancelled']:
            stats['by_workflow'][workflow_name]['failure'] += 1

        # Calculate duration
        if run.get('createdAt') and run.get('updatedAt'):
            created = datetime.fromisoformat(run['createdAt'].replace('Z', '+00:00'))
            updated = datetime.fromisoformat(run['updatedAt'].replace('Z', '+00:00'))
            duration = (updated - created).total_seconds()
            stats['by_workflow'][workflow_name]['total_duration'] += duration

    return stats

def print_report(stats):
    """Print a formatted analysis report"""
    print("=" * 80)
    print("WORKFLOW PERFORMANCE ANALYSIS REPORT")
    print("=" * 80)
    print()

    print(f"Total Workflow Runs: {stats['total_runs']}")
    print()

    print("Status Distribution:")
    for status, count in stats['by_status'].items():
        percentage = (count / stats['total_runs'] * 100) if stats['total_runs'] > 0 else 0
        print(f"  {status}: {count} ({percentage:.1f}%)")
    print()

    print("Conclusion Distribution:")
    for conclusion, count in stats['by_conclusion'].items():
        percentage = (count / stats['total_runs'] * 100) if stats['total_runs'] > 0 else 0
        print(f"  {conclusion}: {count} ({percentage:.1f}%)")
    print()

    print("Performance by Workflow:")
    print("-" * 80)
    for workflow_name, data in stats['by_workflow'].items():
        print(f"\nWorkflow: {workflow_name}")
        print(f"  Total Runs: {data['count']}")
        print(f"  Success: {data['success']}")
        print(f"  Failure: {data['failure']}")
        success_rate = (data['success'] / data['count'] * 100) if data['count'] > 0 else 0
        print(f"  Success Rate: {success_rate:.1f}%")
        avg_duration = data['total_duration'] / data['count'] if data['count'] > 0 else 0
        print(f"  Average Duration: {avg_duration:.0f} seconds ({avg_duration/60:.1f} minutes)")

    print()
    print("=" * 80)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("=" * 80)
    print()

    for workflow_name, data in stats['by_workflow'].items():
        avg_duration = data['total_duration'] / data['count'] if data['count'] > 0 else 0
        avg_minutes = avg_duration / 60

        print(f"\n{workflow_name}:")

        # Timeout recommendations
        recommended_timeout = int(avg_minutes * 2.5)  # 2.5x average for buffer
        print(f"  - Recommended timeout: {recommended_timeout} minutes")
        print(f"    (Based on avg execution time of {avg_minutes:.1f} minutes)")

        # Runner size recommendations
        if avg_minutes < 10:
            print(f"  - Recommended runner: small (current avg: {avg_minutes:.1f}m)")
        elif avg_minutes < 25:
            print(f"  - Recommended runner: medium (current avg: {avg_minutes:.1f}m)")
        else:
            print(f"  - Recommended runner: large (current avg: {avg_minutes:.1f}m)")

        # Success rate recommendations
        success_rate = (data['success'] / data['count'] * 100) if data['count'] > 0 else 0
        if success_rate < 80:
            print(f"  - Warning: Low success rate ({success_rate:.1f}%). Consider investigating failures.")

def main():
    parser = argparse.ArgumentParser(
        description='Analyze GitHub Actions workflow performance'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    parser.add_argument(
        '--workflow',
        type=str,
        help='Specific workflow name to analyze'
    )

    args = parser.parse_args()

    print(f"Fetching workflow runs from the last {args.days} days...")
    runs = get_workflow_runs(args.workflow, args.days)

    if not runs:
        print("No workflow runs found or GitHub CLI not configured.")
        print("Please ensure 'gh' is installed and authenticated.")
        sys.exit(1)

    stats = analyze_runs(runs)
    print_report(stats)

if __name__ == '__main__':
    main()
