from flask import Flask
import requests
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "8814271928:AAG8Db_g6Z4noOEYdLeXe0wzgELDP7ijjNw"
TELEGRAM_CHAT_ID = "8867850194"

@app.route('/')
def run_analyst_evaluation():
    intel_report = (
        f"🏛️ *ANALYST PRE-MARKET STRATEGY MATRIX*\n"
        f"🗓️ Date: {datetime.now().strftime('%d-%b-%Y')} | 08:30 AM IST\n"
        f"────────────────────────\n\n"
        f"✅ GitHub Engine is fully live and connected!"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": intel_report, "parse_mode": "Markdown"}, timeout=10)
    return "Analyst matrix ran successfully.", 200
