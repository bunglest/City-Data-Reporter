"""
reporter.py — Step 3
- Adds fetch_weather() using OpenWeatherMap
- Reads API key from OPENWEATHER_API_KEY
- Handles 401/404/network errors
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict

import requests

API_BASE = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT = 10  # seconds


def get_city_input() -> str:
    while True:
        city = input("Enter a city name: ").strip()
        if city:
            return city
        print("City name cannot be empty. Please try again.")


def fetch_weather(city: str, api_key: str) -> Dict[str, Any]:
    """Call OpenWeatherMap and return JSON or raise RuntimeError with a helpful message."""
    if not api_key:
        raise RuntimeError("Missing OPENWEATHER_API_KEY. See README for setup.")

    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        resp = requests.get(API_BASE, params=params, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise RuntimeError(f"Network error: {exc}") from exc

    if resp.status_code == 401:
        raise RuntimeError("Unauthorized (401): invalid API key.")
    if resp.status_code == 404:
        raise RuntimeError(f"City not found (404): '{city}'.")
    if not resp.ok:
        # Try to include API error message if present
        detail = ""
        try:
            detail = resp.json().get("message", "")
        except Exception:
            pass
        raise RuntimeError(f"OpenWeather error {resp.status_code}: {detail or 'Unexpected error.'}")

    try:
        return resp.json()
    except ValueError as exc:
        raise RuntimeError("Response was not valid JSON.") from exc


def main() -> None:
    city = get_city_input()
    api_key = os.getenv("OPENWEATHER_API_KEY", "")

    try:
        payload = fetch_weather(city, api_key)
        print("Success! Raw payload received.")
        print(str(payload)[:500] + ("..." if len(str(payload)) > 500 else ""))
    except RuntimeError as err:
        print(f"[ERROR] {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
