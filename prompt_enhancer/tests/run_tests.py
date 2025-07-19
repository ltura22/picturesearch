#!/usr/bin/env python3
"""
Test runner for prompt_enhancer module
"""

import sys
import os

# Add the parent directory to the path so we can import prompt_enhancer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_pipeline_tests():
    """Run pipeline tests"""
    print("Running Pipeline Tests...")
    print("=" * 50)
    
    try:
        from .pipeline_tests.test_examples import run_pipeline_tests
        run_pipeline_tests()
        return True
    except Exception as e:
        print(f"Error running pipeline tests: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Prompt Enhancer Test Suite")
    print("=" * 60)
    
    success = True
    
    # Run pipeline tests
    if not run_pipeline_tests():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return success

if __name__ == "__main__":
    run_all_tests() 