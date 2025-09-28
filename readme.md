# 🌆 City Data Reporter

A Python command-line application that reports live weather data for any city using the [OpenWeatherMap API](https://openweathermap.org/api).  

The program validates user input, fetches data from the API, prints a formatted summary, writes results to a CSV file, and provides a summary of all stored cities.




# 🚀 Quickstart

    Clone the repository:

- git clone https://github.com/bunglest/city-data-reporter.git
- cd city-data-reporter


- Install dependencies:
    - python -m pip install requests

## 🔑 Setup: Get an API Key

This project requires an API key from **OpenWeatherMap**.

### 1. Create a free account
- Go to [ OpenWeatherMap Sign Up](https://home.openweathermap.org/users/sign_up).
- Verify your email and log in.

### 2. Generate your API key
- After logging in, go to your [API Keys page](https://home.openweathermap.org/api_keys).
- You will see a **default key** already created for you.  
- You can also create and name a new key (e.g., `city-reporter-key`).

### 3. Save your API key as an environment variable
Your program looks for the variable `OPENWEATHER_API_KEY`.  
Set it once on your system.

**Windows PowerShell:**
```powershell
# Replace with your actual API key from OpenWeatherMap
setx OPENWEATHER_API_KEY "your_api_key_here"

```

## Run the program
    python reporter.py


