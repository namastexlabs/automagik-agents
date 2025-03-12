#!/usr/bin/env python3
"""
Automagik Agents Test Runner

This script runs all available tests for the Automagik Agents system:
- API tests
- CLI tests
- Memory tests

It provides a unified interface for running all tests with options to control
verbosity, output format, and which tests to include.
"""

import argparse
import os
import subprocess
import sys
import json
from datetime import datetime


def setup_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run all Automagik Agents tests")
    
    # Test selection
    parser.add_argument(
        "--api", action="store_true", default=True,
        help="Run API tests (default: True)")
    parser.add_argument(
        "--no-api", action="store_false", dest="api",
        help="Skip API tests")
    parser.add_argument(
        "--cli", action="store_true", default=True,
        help="Run CLI tests (default: True)")
    parser.add_argument(
        "--no-cli", action="store_false", dest="cli",
        help="Skip CLI tests")
    parser.add_argument(
        "--memory", action="store_true", default=True,
        help="Run memory tests (default: True)")
    parser.add_argument(
        "--no-memory", action="store_false", dest="memory",
        help="Skip memory tests")
    
    # Output options
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose output")
    parser.add_argument(
        "--generate-reports", action="store_true", 
        help="Generate test reports (disabled by default)")
    parser.add_argument(
        "--output-dir", default="test_reports",
        help="Directory to store test reports (only used with --generate-reports)")
    parser.add_argument(
        "--html", action="store_true",
        help="Generate HTML reports (only used with --generate-reports)")
    parser.add_argument(
        "--json", action="store_true",
        help="Generate JSON reports (only used with --generate-reports)")
    parser.add_argument(
        "--junit", action="store_true",
        help="Generate JUnit XML reports (only used with --generate-reports)")
    
    # We can add direct execution mode for debugging specific tests
    parser.add_argument(
        "--standalone", action="store_true",
        help="Run tests in standalone mode (without pytest)")
    
    return parser.parse_args()


def ensure_output_dir(output_dir):
    """Ensure the output directory exists."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def run_pytest_tests(args, output_dir=None):
    """Run API endpoint tests using pytest."""
    print("\n\033[1m==== Running API Endpoint Tests with pytest ====\033[0m\n")
    
    cmd = ["pytest", "tests/pytest/test_api_endpoints.py"]
    
    if args.verbose:
        cmd.append("-v")
    
    # Add report options only if report generation is enabled
    if args.generate_reports and output_dir:
        if args.html:
            html_path = os.path.join(output_dir, "test_report.html")
            cmd.append(f"--html={html_path}")
        
        if args.json:
            cmd.append("--json-report")
            json_path = os.path.join(output_dir, "test_results.json")
            cmd.append(f"--json-report-file={json_path}")
            
        if args.junit:
            junit_path = os.path.join(output_dir, "junit_report.xml")
            cmd.append(f"--junitxml={junit_path}")
    
    return subprocess.run(cmd, check=False).returncode


def run_standalone_tests(args, output_dir=None):
    """Run selected tests in standalone mode."""
    print("\n\033[1m==== Running Standalone Tests ====\033[0m\n")
    
    results = {}
    
    if args.api:
        print("\n\033[1m==== Running API Tests ====\033[0m\n")
        cmd = ["python", "tests/standalone/api_test_script.py"]
        if args.verbose:
            cmd.append("--verbose")
        if args.generate_reports and output_dir and args.json:
            json_path = os.path.join(output_dir, "api_results.json")
            cmd.append("--json")
            cmd.append(f"--output={json_path}")
        results["api"] = subprocess.run(cmd, check=False).returncode
    
    if args.cli:
        print("\n\033[1m==== Running CLI Tests ====\033[0m\n")
        cmd = ["python", "tests/standalone/cli_test_script.py", "--all"]
        if args.generate_reports and output_dir and args.json:
            json_path = os.path.join(output_dir, "cli_results.json")
            cmd.append(f"--output={json_path}")
        results["cli"] = subprocess.run(cmd, check=False).returncode
    
    if args.memory:
        print("\n\033[1m==== Running Memory Tests ====\033[0m\n")
        cmd = ["python", "tests/standalone/memory_test_script.py"]
        if args.generate_reports and output_dir and args.json:
            json_path = os.path.join(output_dir, "memory_results.json")
            cmd.append(f"--output={json_path}")
        results["memory"] = subprocess.run(cmd, check=False).returncode
    
    # Return 0 if all tests passed, 1 otherwise
    return 0 if all(code == 0 for code in results.values()) else 1


def main():
    """Main function to run all tests."""
    args = setup_args()
    
    # Create timestamped output directory only if report generation is enabled
    output_dir = None
    if args.generate_reports:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(args.output_dir, timestamp)
        ensure_output_dir(output_dir)
    
    # Run standalone tests first
    standalone_result = run_standalone_tests(args, output_dir)
    
    # Run pytest tests if not in standalone mode
    if not args.standalone and args.api:
        pytest_result = run_pytest_tests(args, output_dir)
    else:
        pytest_result = 0
    
    # Only print the output directory if reports were generated
    if args.generate_reports and output_dir:
        print(f"\nReports saved to: {output_dir}")
    
    # Return non-zero if any test suite failed
    return 1 if standalone_result != 0 or pytest_result != 0 else 0


if __name__ == "__main__":
    sys.exit(main()) 