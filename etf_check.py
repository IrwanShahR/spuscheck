import os
import requests
import pandas as pd
from deepdiff import DeepDiff

ETF_CSV_URL = "https://www.sp-funds.com/wp-content/uploads/data/TidalFG_Holdings_SPUS.csv"
LOCAL_FILE = "last_holdings.csv"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=payload)

def download_csv():
    r = requests.get(ETF_CSV_URL)
    r.raise_for_status()
    with open("new.csv", "wb") as f:
        f.write(r.content)

def compare_and_notify():
    if not os.path.exists(LOCAL_FILE):
        os.rename("new.csv", LOCAL_FILE)
        send_telegram("📥 Initial ETF holdings file saved.")
        return

    old = pd.read_csv(LOCAL_FILE)
    new = pd.read_csv("new.csv")

    diff = DeepDiff(old.to_dict(orient="records"), new.to_dict(orient="records"), ignore_order=True)
    if diff:
        send_telegram("⚠️ ETF Holdings changed!")
        os.replace("new.csv", LOCAL_FILE)
    else:
        print("No changes.")

download_csv()
compare_and_notify()


