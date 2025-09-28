"""
reporter.py — Step 2
- Adds get_city_input() with validation loop
"""

from __future__ import annotations

def get_city_input() -> str:
    """Prompt until a non-empty city name is entered."""
    while True:
        city = input("Enter a city name: ").strip()
        if city:
            return city
        print("City name cannot be empty. Please try again.")

def main() -> None:
    city = get_city_input()
    print(f"Thanks! You entered: {city}")

if __name__ == "__main__":
    main()
