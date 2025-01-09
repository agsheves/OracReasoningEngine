import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import WorldSimulator

def test_create_world():
    """Test world creation functionality"""
    print("\n=== Testing World Creation ===")
    simulator = WorldSimulator()
    test_input = "create world simulation mirror earth December 2023"
    try:
        response = simulator.process_input(test_input)
        print(f"Input: {test_input}")
        parsed_response = json.loads(response)
        print("\nResponse:")
        print(json.dumps(parsed_response, indent=2))
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def test_query_world():
    """Test world querying functionality"""
    print("\n=== Testing World Query ===")
    simulator = WorldSimulator()
    test_input = "query current world state"
    try:
        response = simulator.process_input(test_input)
        print(f"Input: {test_input}")
        parsed_response = json.loads(response)
        print("\nResponse:")
        print(json.dumps(parsed_response, indent=2))
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def run_specific_test(test_name):
    """Run a specific test by name"""
    tests = {
        "create": test_create_world,
        "query": test_query_world
    }

    if test_name in tests:
        print(f"\nRunning test: {test_name}")
        return tests[test_name]()
    else:
        print(f"Test '{test_name}' not found. Available tests: {', '.join(tests.keys())}")
        return False

def run_all_tests():
    """Run all available tests"""
    print("\n=== Running All Tests ===")
    tests = [test_create_world, test_query_world]
    results = []

    for test in tests:
        results.append(test())

    print(f"\nTests completed: {sum(results)} passed, {len(results) - sum(results)} failed")
    return all(results)

if __name__ == "__main__":
    # Check if a specific test was requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        run_specific_test(test_name)
    else:
        print("=== WorldSimulator Test Suite ===")
        print("To run a specific test, use: python tests/test_simulation.py <test_name>")
        print("Available tests: create, query")
        print("Running all tests by default...\n")
        run_all_tests()