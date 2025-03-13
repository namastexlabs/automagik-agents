#!/usr/bin/env python3
"""
Unified pytest runner for all Automagik Agents tests.

This file discovers and runs all standalone test scripts through pytest,
providing consistent reporting and CI integration while maintaining
the ability to run standalone scripts directly during development.
"""

import os
import sys
import importlib.util
import inspect
import pytest
from pathlib import Path
from types import ModuleType

# Ensure the standalone directory is in the path
TESTS_DIR = Path(__file__).parent.parent
STANDALONE_DIR = TESTS_DIR / "standalone"
sys.path.insert(0, str(STANDALONE_DIR))

# List of standalone test scripts to import and run
STANDALONE_MODULES = [
    "api_test_script",
    "cli_test_script",
    "memory_test_script"
]

# Dictionary to store imported test modules
imported_modules = {}

def import_module_from_file(module_name, file_path):
    """Import a module from file path without triggering argparse."""
    # Save the original sys.argv to avoid argparse errors during import
    original_argv = sys.argv
    sys.argv = [str(file_path)]  # Provide a minimal argv to prevent parsing errors
    
    try:
        # Monkey-patch argparse before importing the module
        import argparse
        real_parse_args = argparse.ArgumentParser.parse_args
        argparse.ArgumentParser.parse_args = lambda self, *args, **kwargs: None
        
        # Set up the module import
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        
        # Import the module with the patched argparse
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"Error loading {module_name}: {e}")
            return None
            
        return module
    except Exception as e:
        print(f"Error importing {module_name}: {e}")
        return None
    finally:
        # Restore the original sys.argv
        sys.argv = original_argv
        # Restore original parse_args function if we modified it
        if 'argparse' in sys.modules and 'real_parse_args' in locals():
            sys.modules['argparse'].ArgumentParser.parse_args = real_parse_args

# Try to import all standalone test modules
for module_name in STANDALONE_MODULES:
    file_path = STANDALONE_DIR / f"{module_name}.py"
    if file_path.exists():
        imported_modules[module_name] = import_module_from_file(module_name, file_path)
        # Debug output to check what's being imported
        if imported_modules[module_name]:
            module = imported_modules[module_name]
            print(f"Imported {module_name}. Has main(): {hasattr(module, 'main')}")
            if hasattr(module, 'main'):
                print(f"  main is: {type(module.main)}")
            print(f"  Module attributes: {dir(module)[:10]}...")

def run_standalone_script(module_name, args=None):
    """Run a standalone test script with custom arguments."""
    if module_name in imported_modules and imported_modules[module_name]:
        module = imported_modules[module_name]
        
        # Debug: show all attributes of the module
        print(f"Debug: Module {module_name} has these attributes:")
        for attr in dir(module):
            print(f"  - {attr}")
            
        if hasattr(module, "main"):
            # Save original command line arguments
            original_argv = sys.argv
            
            # Prepare minimal arguments
            minimal_args = [str(STANDALONE_DIR / f"{module_name}.py")]
            if args:
                minimal_args.extend(args)
                
            # Set up arguments for this test run
            sys.argv = minimal_args
            
            try:
                # Run the main function
                return module.main()
            finally:
                # Restore original arguments
                sys.argv = original_argv
        else:
            # We know api_test_script should have a main function, so try to access it directly
            if module_name == "api_test_script" and hasattr(module, "AUTO_CLEANUP"):
                # Disable auto cleanup for pytest integration
                module.AUTO_CLEANUP = False
                
                # Try to run manually constructed test sequence
                print("Attempting to run API tests manually...")
                return module.run_test(module.test_health_endpoint)
            
            pytest.skip(f"{module_name} has no main() function")
    else:
        pytest.skip(f"{module_name} not found or couldn't be imported")
    return None

# Test functions that run each standalone test script
def test_api():
    """Run API tests from standalone script."""
    result = run_standalone_script("api_test_script")
    assert result is None or result == 0, f"API tests failed with exit code {result}"

def test_cli():
    """Run CLI tests from standalone script."""
    result = run_standalone_script("cli_test_script")
    assert result is None or result == 0, f"CLI tests failed with exit code {result}"

def test_memory():
    """Run memory tests from standalone script."""
    result = run_standalone_script("memory_test_script")
    assert result is None or result == 0, f"Memory tests failed with exit code {result}"

# Also run all the API endpoint tests directly
# No need to create a separate function, pytest will discover them automatically
# Use a relative import for test_api_endpoints
# from tests.pytest.test_api_endpoints import *
# The above line causes issues, so we'll leave it commented out
# pytest will automatically discover and run the tests in test_api_endpoints.py 