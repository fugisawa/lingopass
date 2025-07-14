#!/usr/bin/env python3
"""
Test runner script for LingoDash tests
Executes all test suites with coverage reporting
"""

import sys
import subprocess
import os

def run_tests():
    """Run all tests with coverage"""
    
    print("=" * 60)
    print("🧪 Running LingoDash Test Suite")
    print("=" * 60)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Test commands to run
    test_commands = [
        # Run all tests with coverage
        [
            "python", "-m", "pytest", 
            "tests/",
            "-v",  # Verbose output
            "--cov=streamlit_app",  # Coverage for main module
            "--cov-report=html",  # HTML coverage report
            "--cov-report=term-missing",  # Terminal report with missing lines
            "--tb=short",  # Short traceback format
            "-x",  # Stop on first failure
        ],
        
        # Run specific test suites if all pass
        ["python", "-m", "pytest", "tests/test_load_and_charts.py", "-v"],
        ["python", "-m", "pytest", "tests/test_comprehensive.py", "-v"],
        ["python", "-m", "pytest", "tests/test_edge_cases.py", "-v"],
    ]
    
    for i, cmd in enumerate(test_commands):
        print(f"\n📋 Running command {i+1}/{len(test_commands)}:")
        print(" ".join(cmd))
        print("-" * 60)
        
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode != 0:
            print(f"\n❌ Tests failed at command {i+1}")
            return 1
    
    print("\n" + "=" * 60)
    print("✅ All tests passed successfully!")
    print("📊 Coverage report generated in htmlcov/index.html")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(run_tests())