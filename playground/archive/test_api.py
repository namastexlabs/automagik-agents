#!/usr/bin/env python3
"""
Simple utility to test API connectivity.

Usage:
    python playground/test_api.py [API_URL]
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load .env from the root directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    print(f"Loading .env from: {env_path}")
    load_dotenv(dotenv_path=env_path)
    print("Environment variables loaded")
else:
    print(f"Warning: .env file not found at {env_path}")

# Get API URL from command line or environment
if len(sys.argv) > 1:
    api_url = sys.argv[1]
    print(f"Using API URL from command line: {api_url}")
else:
    api_url = os.environ.get("API_BASE_URL", "http://localhost:8000")
    print(f"Using API URL from environment: {api_url}")

# Ensure API URL has protocol
if not api_url.startswith(('http://', 'https://')):
    api_url = f"http://{api_url}"
    print(f"Added http:// protocol: {api_url}")

# List of endpoints to try
endpoints = [
    "/health",
    "/api/health",
    "/",
    "/api",
    "/api/v1",
    "/docs"
]

print(f"\nTesting API connectivity to {api_url}\n")

# Test each endpoint
success = False
for endpoint in endpoints:
    url = f"{api_url}{endpoint}"
    print(f"Testing endpoint: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"  Status code: {response.status_code}")
        
        if response.status_code < 400:
            print(f"  ✅ Success! API is accessible at {url}")
            success = True
            
            # Try to print response content if it's not too large
            try:
                if len(response.text) < 500:
                    print(f"  Response: {response.text}")
                else:
                    print(f"  Response: {response.text[:500]}... (truncated)")
            except:
                pass
        else:
            print(f"  ❌ Error: API returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Error: Could not connect to {url}")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    
    print()

if success:
    print("✅ API connectivity test passed for at least one endpoint")
    sys.exit(0)
else:
    print("❌ API connectivity test failed for all endpoints")
    print("\nTips to resolve API connectivity issues:")
    print("1. Check if the API server is running")
    print("2. Verify the API URL is correct")
    print("3. Check for firewall or network issues")
    print("4. Ensure the API is accessible from your machine")
    sys.exit(1) 