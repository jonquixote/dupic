#!/usr/bin/env python3
"""
Test runner for AI Social Media Manager project
"""

import subprocess
import sys
import os

def run_test_script(script_path, description):
    """Run a test script and return success status"""
    print(f"\n🔍 Running {description}...")
    print("-" * 40)
    
    try:
        # Change to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(project_root)
        
        result = subprocess.run(["python", script_path], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Test completed successfully")
            print(result.stdout)
            return True
        else:
            print("❌ Test failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def main():
    print("🚀 AI Social Media Manager - Test Runner")
    print("=" * 50)
    
    # Define test scripts
    tests = [
        ("tests/unit/verify_implementation.py", "Unit Tests - Implementation Verification"),
        ("tests/integration/test_endpoints.py", "Integration Tests - API Endpoints")
    ]
    
    # Run all tests
    results = []
    for script_path, description in tests:
        success = run_test_script(script_path, description)
        results.append((description, success))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
        print("✅ Implementation is working correctly")
    else:
        print("❌ Some tests failed")
        print("Please review the errors above")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())