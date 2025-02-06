# test_routing.py
# Tests the routing and logic for the web app
# Need to add better tests and process messages

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routing_and_logic import check_shortcode, match_heuristic_with_llm, initial_routing


class TestRouting(unittest.TestCase):
    def test_shortcode_detection(self):
        """Test shortcode detection functionality"""
        print("\n=== Testing Shortcode Detection ===")

        # Test valid shortcodes
        self.assertEqual(check_shortcode("/negotiation"), "negotiation")
        self.assertEqual(check_shortcode("Apply /geopolitics here"), "geopolitics")

        # Test invalid or missing shortcodes
        self.assertIsNone(check_shortcode("No shortcode here"))
        self.assertIsNone(check_shortcode("negotiation"))
        self.assertIsNone(check_shortcode("/invalid"))

    def test_llm_matching(self):
        """Test LLM-based heuristic matching"""
        print("\n=== Testing LLM Matching ===")

        # Test clear matches
        heuristic, settings = match_heuristic_with_llm(
            "We need to negotiate a peace treaty between these nations"
        )
        print(f"Input: Peace treaty negotiation")
        print(f"Matched heuristic: {heuristic}")
        print(f"Settings: {settings}\n")

        # Test ambiguous input
        heuristic, settings = match_heuristic_with_llm("What's the weather like?")
        print(f"Input: Weather query")
        print(f"Matched heuristic: {heuristic}")
        print(f"Settings: {settings}")

    def test_initial_routing(self):
        """Test the main routing function"""
        print("\n=== Testing Initial Routing ===")

        # Test with shortcode
        result = initial_routing("/negotiation test message")
        print(f"Shortcode routing result: {result}\n")

        # Test without shortcode
        result = initial_routing("We need to negotiate a peace treaty")
        print(f"LLM routing result: {result}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
