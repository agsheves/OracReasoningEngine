import json
import sys


def load_heuristics():
    """Load heuristics from JSON file"""
    try:
        with open("heuristics.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: heuristics.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in heuristics.json")
        sys.exit(1)


def list_heuristics(heuristics):
    """List all available heuristics"""
    print("\nAvailable heuristics:")
    for heuristic_id, details in heuristics["heuristics"].items():
        print(f"\n{heuristic_id}:")
        print(f"  Name: {details['name']}")
        print(f"  Description: {details['description']}")


def show_heuristic_details(heuristics, heuristic_id):
    """Show detailed information about a specific heuristic"""
    if heuristic_id not in heuristics["heuristics"]:
        print(f"Error: Heuristic '{heuristic_id}' not found")
        return

    details = heuristics["heuristics"][heuristic_id]
    print(f"\nDetails for {heuristic_id}:")
    print(f"Name: {details['name']}")
    print(f"Description: {details['description']}")

    print("\nParameters:")
    for param, value in details["parameters"].items():
        print(f"  {param}: {value}")

    print("\nMust Do Rules:")
    for rule in details["rules"]["must_do"]:
        print(f"  - {rule}")

    print("\nMust Not Do Rules:")
    for rule in details["rules"]["must_not_do"]:
        print(f"  - {rule}")


def main():
    heuristics = load_heuristics()

    while True:
        print("\n=== Heuristics Testing Tool ===")
        print("1. List all heuristics")
        print("2. Show details for a specific heuristic")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            list_heuristics(heuristics)
        elif choice == "2":
            heuristic_id = input("Enter heuristic ID (e.g., 'trading_strategy'): ")
            show_heuristic_details(heuristics, heuristic_id)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
