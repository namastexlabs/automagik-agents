#!/usr/bin/env python3
"""
Memory Test Script for Automagik-Agents

This script tests the memory capabilities of agents by engaging in a sequential
conversation and checking if context is maintained throughout the session.
"""

import subprocess
import json
import sys
import re
import os
import time
import argparse
from typing import Optional, List, Dict, Any, Tuple

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

def print_step(step: str, message: str) -> None:
    """Print a formatted step message."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[STEP {step}] {message}{Colors.ENDC}")

def print_user_message(message: str) -> None:
    """Print a formatted user message."""
    print(f"{Colors.BLUE}User → {message}{Colors.ENDC}")

def print_agent_message(message: str) -> None:
    """Print a formatted agent message."""
    print(f"{Colors.GREEN}Agent → {message}{Colors.ENDC}")

def print_result(success: bool, message: str) -> None:
    """Print a test result."""
    if success:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ PASS: {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}✗ FAIL: {message}{Colors.ENDC}")

def extract_assistant_response(output: str) -> Optional[str]:
    """Extract the assistant's response text from the command output."""
    # Try to find the assistant response line after "assistant:"
    assistant_pattern = r"assistant:\s*(.*)"
    match = re.search(assistant_pattern, output)
    if match:
        return match.group(1).strip()
    
    # Alternative pattern in case the output format changes
    alt_pattern = r"\[Tool\].*?\n(.*)"
    match = re.search(alt_pattern, output)
    if match:
        return match.group(1).strip()
    
    return None

def run_message_command(agent: str, message: str, session: str, debug: bool = False) -> Tuple[str, Optional[str]]:
    """
    Run the agent message command and return the output and extracted response.
    
    Args:
        agent: Name of the agent to use
        message: Message to send
        session: Session name for the conversation
        debug: Whether to run in debug mode
    
    Returns:
        Tuple of (full command output, extracted assistant response)
    """
    debug_flag = "--debug" if debug else ""
    command = f"automagik-agents {debug_flag} agent run message --agent {agent} --message \"{message}\" --session {session}"
    print_user_message(message)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        assistant_response = extract_assistant_response(output)
        
        if assistant_response:
            print_agent_message(assistant_response)
        else:
            print(f"{Colors.WARNING}Could not extract assistant response. Full output:{Colors.ENDC}")
            print(output)
            
        return output, assistant_response
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}Command failed with error:{Colors.ENDC}")
        print(e.stderr)
        return e.stderr, None

def run_memory_test(agent_name: str = "simple_agent", user_name: str = "Felipe", session_name: str = None, debug: bool = False) -> bool:
    """
    Run the complete memory test sequence.
    
    Args:
        agent_name: Name of the agent to test
        user_name: Name to use in the test
        session_name: Optional custom session name (default: generated)
        debug: Whether to run in debug mode
    
    Returns:
        True if all tests passed, False otherwise
    """
    if not session_name:
        session_name = f"memory-test-{int(time.time())}"

    print_header(f"MEMORY TEST: Testing {agent_name} with session '{session_name}'")
    
    test_results = []
    
    # Step 1: Introduce with name
    print_step("1", "Introducing with name")
    intro_message = f"My name is {user_name}"
    _, intro_response = run_message_command(agent_name, intro_message, session_name, debug)
    
    if not intro_response:
        print_result(False, "Failed to get response to introduction")
        test_results.append(False)
    else:
        print_result(True, "Introduction successful")
        test_results.append(True)
    
    # Step 2: Start counting sequence
    print_step("2", "Starting counting sequence")
    count_message = "Continue the next number: 1"
    _, count_response = run_message_command(agent_name, count_message, session_name, debug)
    
    # Check if response contains "2"
    contains_correct_number = count_response and "2" in count_response
    print_result(contains_correct_number, "Agent correctly responded with number 2")
    test_results.append(contains_correct_number)
    
    # Step 3: Continue counting with "3"
    print_step("3", "Continuing count with '3'")
    _, count3_response = run_message_command(agent_name, "3", session_name, debug)
    
    # Check if response contains "4"
    contains_4 = count3_response and "4" in count3_response
    print_result(contains_4, "Agent correctly responded with number 4")
    test_results.append(contains_4)
    
    # Step 4: Continue counting with "5"
    print_step("4", "Continuing count with '5'")
    _, count5_response = run_message_command(agent_name, "5", session_name, debug)
    
    # Check if response contains "6"
    contains_6 = count5_response and "6" in count5_response
    print_result(contains_6, "Agent correctly responded with number 6")
    test_results.append(contains_6)
    
    # Step 5: Check if agent remembers the name
    print_step("5", "Checking if agent remembers the name")
    _, name_response = run_message_command(agent_name, "What's my name?", session_name, debug)
    
    # Check if response contains the user's name
    remembers_name = name_response and user_name.lower() in name_response.lower()
    print_result(remembers_name, f"Agent remembers the name '{user_name}'")
    test_results.append(remembers_name)
    
    # Final summary
    all_passed = all(test_results)
    print_header("TEST SUMMARY")
    print(f"Session: {session_name}")
    print(f"Agent: {agent_name}")
    
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}All memory tests PASSED!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}Some memory tests FAILED!{Colors.ENDC}")
        
        # Detailed results
        steps = [
            "Introduction response",
            "Counting sequence (1→2)",
            "Counting sequence (3→4)",
            "Counting sequence (5→6)",
            "Name recall"
        ]
        
        for i, (step, result) in enumerate(zip(steps, test_results)):
            status = f"{Colors.GREEN}PASS{Colors.ENDC}" if result else f"{Colors.FAIL}FAIL{Colors.ENDC}"
            print(f"  Step {i+1}: {step} - {status}")
    
    return all_passed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run memory tests for Automagik Agents")
    parser.add_argument("--agent", default="simple_agent", help="Agent to test")
    parser.add_argument("--user-name", default="Felipe", help="User name to use in the test")
    parser.add_argument("--session", help="Custom session name (default: auto-generated)")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    args = parser.parse_args()
    
    success = run_memory_test(
        agent_name=args.agent,
        user_name=args.user_name,
        session_name=args.session,
        debug=args.debug
    )
    
    # Exit with appropriate code for CI/CD pipelines
    sys.exit(0 if success else 1) 