"""
reporter.py — Step 4
- Adds parse_weather() to extract fields
- Prints a clean summary to console
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


def parse_weather(payload: Dict[str, Any]) -> Dict[str, str]:
    """Return City, Country, Temperature (C), Humidity (%), Description."""
    try:
        city = payload["name"]
        country = payload["sys"]["country"]
        temp_c = float(payload["main"]["temp"])
        humidity = int(payload["main"]["humidity"])
        description = str(payload["weather"][0]["description"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise RuntimeError("API payload missing expected fields.") from exc

    return {
        "City": city,
        "Country": country,
        "Temperature (C)": f"{temp_c:.1f}",
        "Humidity (%)": str(humidity),
        "Description": description,
    }


def main() -> None:
    city = get_city_input()
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    try:
        data = parse_weather(fetch_weather(city, api_key))
    except RuntimeError as err:
        print(f"[ERROR] {err}")
        sys.exit(1)

    print(
        f"\nCurrent weather for {data['City']}, {data['Country']}:\n"
        f"- Temperature: {data['Temperature (C)']} °C\n"
        f"- Humidity: {data['Humidity (%)']}%\n"
        f"- Description: {data['Description']}\n"
    )


if __name__ == "__main__":
    main()
