#!/usr/bin/env python3
"""
Test runner for prompt_enhancer module
"""

import sys
import os

# Add the parent directory to the path so we can import prompt_enhancer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_pipeline_tests(test_numbers=None):
    """Run pipeline tests"""
    print("Running Pipeline Tests...")
    print("=" * 50)
    
    try:
        from .pipeline_tests.test_examples import run_pipeline_tests
        run_pipeline_tests(test_numbers)
        return True
    except Exception as e:
        print(f"Error running pipeline tests: {e}")
        return False

def run_structure_tests():
    """Run structure tests"""
    print("Running Structure Tests...")
    print("=" * 50)
    
    try:
        from .pipeline_tests.test_structure import test_structure, test_examples
        test_structure()
        test_examples()
        return True
    except Exception as e:
        print(f"Error running structure tests: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Prompt Enhancer Test Suite")
    print("=" * 60)
    
    success = True
    
    # Run structure tests
    if not run_structure_tests():
        success = False
    
    print("\n" + "=" * 60)
    
    # Run pipeline tests
    if not run_pipeline_tests():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return success

def show_help():
    """Show help information"""
    print("Prompt Enhancer Test Runner")
    print("=" * 40)
    print("Usage:")
    print("  python -m prompt_enhancer.tests.run_tests [options]")
    print("")
    print("Options:")
    print("  --all                    Run all tests (default)")
    print("  --pipeline [numbers]     Run pipeline tests only")
    print("  --structure              Run structure tests only")
    print("  --help                   Show this help")
    print("")
    print("Pipeline test numbers:")
    print("  --pipeline 1,2,3         Run specific tests")
    print("  --pipeline 4-8           Run range of tests")
    print("  --pipeline 3,5,6,7       Run specific tests")
    print("")
    print("Examples:")
    print("  python -m prompt_enhancer.tests.run_tests")
    print("  python -m prompt_enhancer.tests.run_tests --pipeline 1,2,3")
    print("  python -m prompt_enhancer.tests.run_tests --pipeline 4-8")
    print("  python -m prompt_enhancer.tests.run_tests --structure")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments, run all tests
        run_all_tests()
    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        show_help()
    elif sys.argv[1] == "--structure":
        run_structure_tests()
    elif sys.argv[1] == "--pipeline":
        if len(sys.argv) > 2:
            # Parse test numbers
            from .pipeline_tests.test_examples import parse_test_numbers
            test_numbers = parse_test_numbers(sys.argv[2])
            if test_numbers:
                print(f"Running pipeline tests: {test_numbers}")
                run_pipeline_tests(test_numbers)
            else:
                print("Invalid test specification. Use format like '1,2,3' or '4-8'")
        else:
            # Run all pipeline tests
            run_pipeline_tests()
    elif sys.argv[1] == "--all":
        run_all_tests()
    else:
        print("Unknown option. Use --help for usage information.")
        sys.exit(1) 