#!/usr/bin/env python3
"""
Test script to verify that all AI Social Media Manager endpoints are working
"""

import requests
import json
import time
import os

# Base URL for the API
BASE_URL = "http://localhost:5000/api"

def test_endpoint(url, method="GET", data=None, expected_status=200):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == expected_status:
            print(f"✅ {method} {url} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ {method} {url} - Status: {response.status_code}, Expected: {expected_status}")
            print(f"   Response: {response.text[:100]}...")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {url} - Error: {str(e)}")
        return False

def main():
    print("🧪 Testing AI Social Media Manager API Endpoints")
    print("=" * 50)
    
    # Test health check
    test_endpoint(f"{BASE_URL}/health")
    
    # Test AI providers
    test_endpoint(f"{BASE_URL}/ai_providers")
    
    # Test trends endpoints
    test_endpoint(f"{BASE_URL}/trends")
    test_endpoint(f"{BASE_URL}/trends/top")
    test_endpoint(f"{BASE_URL}/trends/refresh", method="POST")
    
    # Test characters endpoints
    test_endpoint(f"{BASE_URL}/characters/templates")
    
    # Test content generation endpoints
    test_endpoint(f"{BASE_URL}/content/generate", method="POST", data={
        "trend_id": 1,
        "character_id": 1,
        "provider": "openai",
        "model": "gpt-4o-mini"
    }, expected_status=400)  # Expected to fail due to missing data
    
    # Test user analytics endpoints
    test_endpoint(f"{BASE_URL}/user_analytics", method="POST", data={
        "user_id": 1,
        "metric_name": "test_metric",
        "value": "test_value"
    })
    
    # Test favorite content endpoints
    test_endpoint(f"{BASE_URL}/favorite_content", method="POST", data={
        "user_id": 1,
        "content_id": "test_content_123"
    })
    
    print("\n" + "=" * 50)
    print("🧪 Test completed. Check results above.")

if __name__ == "__main__":
    # Change to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(project_root)
    main()