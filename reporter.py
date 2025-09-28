"""
reporter.py — Step 7 (polished)
City Data Reporter: prompt for a city, fetch live weather from OpenWeatherMap,
print a summary, write to CSV, and summarize the CSV contents.

- PEP 8 naming and structure
- Docstrings and type hints
"""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests

API_BASE = "https://api.openweathermap.org/data/2.5/weather"
TIMEOUT = 10
CSV_PATH = Path("city_data.csv")


def get_city_input() -> str:
    """Prompt until a non-empty city name is entered."""
    while True:
        city = input("Enter a city name: ").strip()
        if city:
            return city
        print("City name cannot be empty. Please try again.")


def fetch_weather(city: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch weather data from OpenWeatherMap.

    Raises:
        RuntimeError: If the API key is missing, city not found, or network/API issues occur.
    """
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
    """
    Extract key fields for reporting and CSV writing.
    Returns:
        Dict with keys: City, Country, Temperature (C), Humidity (%), Description
    """
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


def ensure_csv_headers(path: Path) -> None:
    """Create CSV with headers if not present or empty."""
    headers = ["City", "Country", "Temperature (C)", "Humidity (%)", "Description"]
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)


def write_row_to_csv(row: Dict[str, str], path: Path = CSV_PATH) -> None:
    """Append a row to the CSV, ensuring headers exist."""
    ensure_csv_headers(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(
            [row["City"], row["Country"], row["Temperature (C)"], row["Humidity (%)"], row["Description"]]
        )


def summarize_csv(path: Path = CSV_PATH) -> Optional[str]:
    """Return a human-readable summary of the CSV contents, or None if empty/missing."""
    if not path.exists():
        return None
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return None
    lines = [f"Total entries: {len(rows)}"]
    for r in rows:
        lines.append(f"- {r.get('City','?')} — {r.get('Temperature (C)','?')} °C")
    return "\n".join(lines)


def main() -> None:
    """Entrypoint: prompt, fetch, parse, print, save, summarize."""
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

    try:
        write_row_to_csv(data, CSV_PATH)
        print(f"Saved to {CSV_PATH.resolve()}")
    except OSError as err:
        print(f"[WARNING] Could not write to CSV: {err}")

    summary = summarize_csv(CSV_PATH)
    if summary:
        print("\nCSV Summary:")
        print(summary)


if __name__ == "__main__":
    main()
