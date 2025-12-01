
#!/usr/bin/env python3
"""Quick test runner for development"""

import subprocess
import sys

def run_quick_tests():
    """Run fast tests only"""
    print("🧪 Running quick tests (excluding slow tests)...\n")
    
    result = subprocess.run(
        ["pytest", "tests/", "-v", "-m", "not slow", "--tb=short"],
        capture_output=False
    )
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_quick_tests())
