import os
import requests
import pandas as pd
import time
from utils.logging_utils import log_change
from config import *

# Fetch historical data from API
def fetch_historical_data(symbol, interval, start, end, API_URL):
    params = {
        "symbol": symbol,
        "type": interval,
        "startAt": start,
        "endAt": end
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        log_change(f"Error fetching data: {response.text}")
        return None

# Update historical data
def update_historical_data(symbol, interval, DATA_PATH):
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH, parse_dates=["time"])
        last_time = int(df["time"].iloc[-1].timestamp())
    else:
        last_time = int(time.time()) - 60 * 60 * 24 * 90
        df = pd.DataFrame(columns=["time", "open", "close", "high", "low", "volume", "turnover"])

    current_time = int(time.time())
    new_data = []

    while last_time < current_time:
        request_end_time = min(last_time + 1500 * 60 * 60, current_time)
        data = fetch_historical_data(symbol, interval, last_time, request_end_time, API_URL)
        print(symbol, interval, last_time, request_end_time, API_URL)
        if data:
            new_data.extend(data)
            last_time = request_end_time
        else:
            log_change("Error fetching new data. Stopping update.")
            break

    if new_data:
        new_df = pd.DataFrame(new_data, columns=["time", "open", "close", "high", "low", "volume", "turnover"])
        new_df["time"] = pd.to_datetime(new_df["time"], unit='s')
        new_df["close"] = new_df["close"].astype(float)
        new_df["volume"] = new_df["volume"].astype(float)
        df = pd.concat([df, new_df]).drop_duplicates(subset="time").sort_values(by="time")
        df.to_csv(DATA_PATH, index=False)
        log_change(f"Historical data updated. {len(new_df)} new rows added.")
    else:
        log_change("No new data added. Historical data is up to date.")

    return df