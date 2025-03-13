#!/usr/bin/env python3
"""
CLI Test Script for Automagik-Agents

This script tests all available CLI commands in the automagik-agents package
and provides a comprehensive test report.
"""

import subprocess
import json
import sys
import re
import os
import argparse
import time
from typing import Optional, List, Dict, Any, Tuple, Callable

# Terminal colors for better output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message: str) -> None:
    """Print a formatted header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD} {message} {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_subheader(message: str) -> None:
    """Print a formatted subheader message."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'-'*60}{Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD} {message} {Colors.ENDC}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'-'*60}{Colors.ENDC}\n")

def print_command(command: str) -> None:
    """Print a formatted command."""
    print(f"{Colors.BLUE}$ {command}{Colors.ENDC}")

def print_result(success: bool, message: str) -> None:
    """Print a test result."""
    if success:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ PASS: {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}✗ FAIL: {message}{Colors.ENDC}")

def run_command(command: str, expected_success: bool = True, 
                expected_output: Optional[str] = None,
                expected_output_pattern: Optional[str] = None,
                timeout: int = 10,
                capture_stderr: bool = True) -> Tuple[bool, str]:
    """
    Run a CLI command and check the result.
    
    Args:
        command: Command to run
        expected_success: Whether the command is expected to succeed
        expected_output: String that should be in the output
        expected_output_pattern: Regex pattern to match in output
        timeout: Command timeout in seconds
        capture_stderr: Whether to capture stderr in the output
    
    Returns:
        Tuple of (success, output)
    """
    print_command(command)
    
    stderr_pipe = subprocess.STDOUT if capture_stderr else subprocess.PIPE
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=stderr_pipe,
            text=True,
            timeout=timeout
        )
        output = result.stdout

        # Print abbreviated output (first 10 lines and last 5 lines)
        output_lines = output.splitlines()
        shortened_output = []
        
        if len(output_lines) > 15:
            shortened_output = output_lines[:10]
            shortened_output.append(f"... ({len(output_lines) - 15} more lines) ...")
            shortened_output.extend(output_lines[-5:])
            print("\n".join(shortened_output))
        else:
            print(output)
        
        # Check if command succeeded as expected
        success_matches = (result.returncode == 0) == expected_success
        
        # Check output constraints
        output_match = True
        if expected_output and expected_output not in output:
            output_match = False
            
        pattern_match = True
        if expected_output_pattern and not re.search(expected_output_pattern, output):
            pattern_match = False
            
        return success_matches and output_match and pattern_match, output
    except subprocess.TimeoutExpired:
        print(f"{Colors.WARNING}Command timed out after {timeout} seconds{Colors.ENDC}")
        return False, f"TIMEOUT: Command did not complete within {timeout} seconds"
    except Exception as e:
        print(f"{Colors.FAIL}Error executing command: {str(e)}{Colors.ENDC}")
        return False, f"ERROR: {str(e)}"

def test_global_options() -> List[Dict[str, Any]]:
    """Test global CLI options."""
    print_header("Testing Global Options")
    results = []
    
    # Test --help option
    cmd = "automagik-agents --help"
    success, output = run_command(cmd, expected_output="Usage:")
    print_result(success, "Global --help option")
    results.append({
        "command": cmd,
        "success": success,
        "description": "Global --help option"
    })
    
    # Test --debug option - Updated to match actual output
    cmd = "automagik-agents --debug --help"
    success, output = run_command(cmd, expected_output="Debug mode enabled")
    print_result(success, "Global --debug option")
    results.append({
        "command": cmd,
        "success": success,
        "description": "Global --debug option"
    })
    
    # Test show-completion - Make it expect failure for unsupported shells
    cmd = "automagik-agents --show-completion"
    success, output = run_command(cmd, expected_success=False, expected_output_pattern=r"Shell .* not supported|Available shell completion")
    print_result(success, "Global --show-completion option")
    results.append({
        "command": cmd,
        "success": success,
        "description": "Global --show-completion option"
    })
    
    return results

def test_api_commands() -> List[Dict[str, Any]]:
    """Test API server commands."""
    print_header("Testing API Commands")
    results = []
    
    # Test api start (with short timeout to avoid hanging)
    print_subheader("Testing api start (with --help to avoid actual server start)")
    cmd = "automagik-agents api start --help"
    success, output = run_command(cmd, expected_output="Start the FastAPI server")
    print_result(success, "api start --help command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "api start --help command"
    })
    
    # We won't actually start the server to avoid hanging the test script
    # Instead we'll just test the options
    options = ["--host", "--port", "--reload", "--workers"]
    for option in options:
        cmd = f"automagik-agents api start --help"
        success, output = run_command(cmd, expected_output=option)
        print_result(success, f"api start {option} option exists")
        results.append({
            "command": cmd,
            "success": success,
            "description": f"api start {option} option exists"
        })
    
    return results

def test_db_commands() -> List[Dict[str, Any]]:
    """Test database commands."""
    print_header("Testing Database Commands")
    results = []
    
    # Test db init help
    print_subheader("Testing db init (help only)")
    cmd = "automagik-agents db init --help"
    success, output = run_command(cmd, expected_output="Initialize the database")
    print_result(success, "db init --help command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "db init --help command"
    })
    
    # Test db init force option exists
    cmd = "automagik-agents db init --help"
    success, output = run_command(cmd, expected_output="--force")
    print_result(success, "db init --force option exists")
    results.append({
        "command": cmd,
        "success": success,
        "description": "db init --force option exists"
    })
    
    # Test db reset help
    print_subheader("Testing db reset (help only)")
    cmd = "automagik-agents db reset --help"
    success, output = run_command(cmd, expected_output="Reset the database")
    print_result(success, "db reset --help command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "db reset --help command"
    })
    
    # Test db reset yes option exists
    cmd = "automagik-agents db reset --help"
    success, output = run_command(cmd, expected_output="--yes")
    print_result(success, "db reset --yes option exists")
    results.append({
        "command": cmd,
        "success": success,
        "description": "db reset --yes option exists"
    })
    
    return results

def test_agent_chat_commands() -> List[Dict[str, Any]]:
    """Test agent chat commands."""
    print_header("Testing Agent Chat Commands")
    results = []
    
    # Test agent chat list
    print_subheader("Testing agent chat list")
    cmd = "automagik-agents agent chat list"
    success, output = run_command(cmd, expected_output_pattern=r"(agent|available)")
    print_result(success, "agent chat list command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent chat list command"
    })
    
    # Test agent chat start help (to avoid actual chat session) - Updated to match actual output
    print_subheader("Testing agent chat start (help only)")
    cmd = "automagik-agents agent chat start --help"
    success, output = run_command(cmd, expected_output="Start an interactive chat session")
    print_result(success, "agent chat start --help command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent chat start --help command"
    })
    
    # Test agent chat start options
    options = ["--agent", "--session", "--user"]
    for option in options:
        cmd = f"automagik-agents agent chat start --help"
        success, output = run_command(cmd, expected_output=option)
        print_result(success, f"agent chat start {option} option exists")
        results.append({
            "command": cmd,
            "success": success,
            "description": f"agent chat start {option} option exists"
        })
    
    return results

def test_agent_run_commands() -> List[Dict[str, Any]]:
    """Test agent run commands."""
    print_header("Testing Agent Run Commands")
    results = []
    
    # Test agent run list
    print_subheader("Testing agent run list")
    cmd = "automagik-agents agent run list"
    success, output = run_command(cmd, expected_output_pattern=r"(agent|available)")
    print_result(success, "agent run list command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent run list command"
    })
    
    # Test agent run message help
    print_subheader("Testing agent run message (help only)")
    cmd = "automagik-agents agent run message --help"
    success, output = run_command(cmd, expected_output="Run a single message")
    print_result(success, "agent run message --help command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent run message --help command"
    })
    
    # Test agent run message options
    options = ["--agent", "--session", "--user", "--message"]
    for option in options:
        cmd = f"automagik-agents agent run message --help"
        success, output = run_command(cmd, expected_output=option)
        print_result(success, f"agent run message {option} option exists")
        results.append({
            "command": cmd,
            "success": success,
            "description": f"agent run message {option} option exists"
        })
    
    # Test actual message running with simple message
    print_subheader("Testing agent run message with actual message")
    cmd = f"automagik-agents agent run message --agent simple_agent --message \"Hello\""
    success, output = run_command(
        cmd, 
        expected_output_pattern=r"(response|message|assistant)",
        timeout=30  # Allow more time for actual API calls
    )
    print_result(success, "agent run message with simple message")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent run message with simple message"
    })
    
    return results

def test_agent_create_commands() -> List[Dict[str, Any]]:
    """Test agent create commands."""
    print_header("Testing Agent Create Commands")
    results = []
    
    # Test agent create list-templates
    print_subheader("Testing agent create list-templates")
    cmd = "automagik-agents agent create list-templates"
    success, output = run_command(cmd, expected_output_pattern=r"(template|agent)")
    print_result(success, "agent create list-templates command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent create list-templates command"
    })
    
    # Test agent create list-categories
    print_subheader("Testing agent create list-categories")
    cmd = "automagik-agents agent create list-categories"
    success, output = run_command(cmd, expected_output_pattern=r"(categor|folder)")
    print_result(success, "agent create list-categories command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent create list-categories command"
    })
    
    # Test agent create list
    print_subheader("Testing agent create list")
    cmd = "automagik-agents agent create list"
    success, output = run_command(cmd, expected_output_pattern=r"(template|categor|agent)")
    print_result(success, "agent create list command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent create list command"
    })
    
    # Test agent create agent help
    print_subheader("Testing agent create agent (help only)")
    cmd = "automagik-agents agent create agent --help"
    success, output = run_command(cmd, expected_output="Create a new agent")
    print_result(success, "agent create agent --help command")
    results.append({
        "command": cmd,
        "success": success,
        "description": "agent create agent --help command"
    })
    
    # Test agent create agent options
    options = ["--name", "--category", "--template"]
    for option in options:
        cmd = f"automagik-agents agent create agent --help"
        success, output = run_command(cmd, expected_output=option)
        print_result(success, f"agent create agent {option} option exists")
        results.append({
            "command": cmd,
            "success": success,
            "description": f"agent create agent {option} option exists"
        })
    
    return results

def execute_all_tests(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Execute all CLI tests.
    
    Args:
        args: Command line arguments
        
    Returns:
        Dictionary with test results
    """
    test_results = {
        "global_options": [],
        "api_commands": [],
        "db_commands": [],
        "agent_chat_commands": [],
        "agent_run_commands": [],
        "agent_create_commands": []
    }
    
    if args.all or args.global_options:
        test_results["global_options"] = test_global_options()
    
    if args.all or args.api:
        test_results["api_commands"] = test_api_commands()
    
    if args.all or args.db:
        test_results["db_commands"] = test_db_commands()
    
    if args.all or args.agent_chat:
        test_results["agent_chat_commands"] = test_agent_chat_commands()
    
    if args.all or args.agent_run:
        test_results["agent_run_commands"] = test_agent_run_commands()
    
    if args.all or args.agent_create:
        test_results["agent_create_commands"] = test_agent_create_commands()
    
    return test_results

def print_summary(results: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Print a summary of all test results.
    
    Args:
        results: Test results dictionary
    """
    print_header("TEST SUMMARY")
    
    total_tests = 0
    total_passed = 0
    
    for category, tests in results.items():
        if not tests:
            continue
            
        category_passed = sum(1 for test in tests if test["success"])
        total_tests += len(tests)
        total_passed += category_passed
        
        category_name = category.replace("_", " ").title()
        success_rate = (category_passed / len(tests)) * 100 if tests else 0
        
        if success_rate == 100:
            print(f"{Colors.GREEN}{category_name}: {category_passed}/{len(tests)} ({success_rate:.1f}%){Colors.ENDC}")
        elif success_rate >= 80:
            print(f"{Colors.WARNING}{category_name}: {category_passed}/{len(tests)} ({success_rate:.1f}%){Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}{category_name}: {category_passed}/{len(tests)} ({success_rate:.1f}%){Colors.ENDC}")
            
        # List failed tests in this category
        if category_passed < len(tests):
            print(f"  Failed tests:")
            for test in tests:
                if not test["success"]:
                    print(f"  {Colors.FAIL}- {test['description']}{Colors.ENDC}")
    
    # Overall success rate
    overall_rate = (total_passed / total_tests) * 100 if total_tests else 0
    print(f"\n{Colors.BOLD}Overall: {total_passed}/{total_tests} ({overall_rate:.1f}%){Colors.ENDC}")
    
    if overall_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}Some tests failed. Review the output for details.{Colors.ENDC}")

def save_results(results: Dict[str, List[Dict[str, Any]]], output_file: str) -> None:
    """
    Save test results to a JSON file.
    
    Args:
        results: Test results dictionary
        output_file: Path to the output file
    """
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CLI tests for Automagik Agents")
    
    # Test selection options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--global-options", action="store_true", help="Test global CLI options")
    parser.add_argument("--api", action="store_true", help="Test API commands")
    parser.add_argument("--db", action="store_true", help="Test database commands")
    parser.add_argument("--agent-chat", action="store_true", help="Test agent chat commands")
    parser.add_argument("--agent-run", action="store_true", help="Test agent run commands")
    parser.add_argument("--agent-create", action="store_true", help="Test agent create commands")
    
    # Output options
    parser.add_argument("--output", "-o", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    # If no specific test is selected, run all tests
    if not any([args.all, args.global_options, args.api, args.db, 
                args.agent_chat, args.agent_run, args.agent_create]):
        args.all = True
    
    # Run all tests and get results
    start_time = time.time()
    results = execute_all_tests(args)
    end_time = time.time()
    
    # Print summary
    print_summary(results)
    print(f"\nTests completed in {end_time - start_time:.2f} seconds")
    
    # Save results if output file specified
    if args.output:
        save_results(results, args.output)
    
    # Exit with appropriate code for CI/CD pipelines
    all_passed = all(test["success"] for category in results.values() for test in category)
    sys.exit(0 if all_passed else 1) 