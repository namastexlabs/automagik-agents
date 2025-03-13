#!/usr/bin/env python3
"""
Automagik Agents API Test Runner

This script runs API tests for the Automagik Agents system, providing a unified
interface for running either the standalone script or the pytest suite.

Usage:
    python tests/run_api_tests.py [options]

Options:
    --mode=MODE      Test mode: 'standalone' or 'pytest' (default: pytest)
    --verbose, -v    Enable verbose output
    --json, -j       Output results as JSON (for AI consumption)
    --html=PATH      Generate HTML report (pytest mode only)
    --junit=PATH     Generate JUnit XML report (pytest mode only)
    --url=URL        Specify the base URL for testing
    --help, -h       Show this help message

Examples:
    python tests/run_api_tests.py --mode=pytest --verbose
    python tests/run_api_tests.py --mode=standalone --json
    python tests/run_api_tests.py --html=report.html
"""

import argparse
import os
import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path


def setup_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run API tests for Automagik Agents")
    
    parser.add_argument(
        "--mode", choices=["pytest", "standalone"], default="pytest",
        help="Test mode: pytest or standalone (default: pytest)")
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose output")
    
    parser.add_argument(
        "--html", 
        help="Generate HTML report (pytest mode only)")
    parser.add_argument(
        "--junit", 
        help="Generate JUnit XML report (pytest mode only)")
    parser.add_argument(
        "--json", action="store_true",
        help="Generate JSON output")
    parser.add_argument(
        "--output",
        help="Output file for JSON results (if --json is specified)")
    
    parser.add_argument(
        "--url",
        help="Base URL for API (overrides .env)")
    
    return parser.parse_args()


def ensure_output_dir(output_path):
    """Ensure the output directory exists."""
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)


def run_pytest_tests(args):
    """Run API tests using pytest."""
    print("\n\033[1m==== Running API Tests (pytest) ====\033[0m\n")
    
    cmd = ["pytest", "tests/pytest/test_api_endpoints.py"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.json:
        cmd.append("--json-report")
        if args.output:
            cmd.append(f"--json-report-file={args.output}")
    
    if args.html:
        cmd.append(f"--html={args.html}")
        
    if args.junit:
        cmd.append(f"--junitxml={args.junit}")
    
    if args.url:
        cmd.append(f"--url={args.url}")
    
    return subprocess.run(cmd, check=False).returncode


def run_standalone_tests(args):
    """Run API tests using the standalone script."""
    print("\n\033[1m==== Running API Tests (standalone) ====\033[0m\n")
    
    cmd = ["python", "tests/standalone/api_test_script.py"]
    
    if args.verbose:
        cmd.append("--verbose")
    
    if args.json:
        cmd.append("--json")
        
    if args.output:
        cmd.append(f"--output={args.output}")
    
    if args.url:
        cmd.append(f"--url={args.url}")
    
    return subprocess.run(cmd, check=False).returncode


def main():
    """Main function to run API tests."""
    args = setup_args()
    
    # Ensure output directory exists if needed
    if args.output:
        ensure_output_dir(args.output)
    if args.html:
        ensure_output_dir(args.html)
    if args.junit:
        ensure_output_dir(args.junit)
    
    # Run tests based on the selected mode
    if args.mode == "pytest":
        return run_pytest_tests(args)
    else:
        return run_standalone_tests(args)


if __name__ == "__main__":
    sys.exit(main()) 