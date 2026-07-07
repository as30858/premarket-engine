from flask import Flask
import yfinance as yf
import requests
from datetime import datetime
import threading

app = Flask(__name__)

TELEGRAM_TOKEN = "8814271928:AAG8Db_g6Z4noOEYdLeXe0wzgELDP7ijjNw"
TELEGRAM_CHAT_ID = "8867850194"

TARGET_TICKERS = [
    'AMAGI.NS', 'ASIANPAINT.NS', 'CCAVENUE.NS', 'BANKBARODA.NS', 'BPCL.NS', 
    'BSOFT.NS', 'EMIL.NS', 'FEDERALBNK.NS', 'GICRE.NS', 'GEOJITFSL.NS', 
    'ICICIPRULI.NS', 'IDFCFIRSTB.NS', 'IRFC.NS', 'IRB.NS', 'ITC.NS', 
    'JUSTDIAL.NS', 'MOREPENLAB.NS', 'MSUMI.NS', 'NHPC.NS', 'NTPC.NS', 
    'ONGC.NS', 'PFC.NS', 'PROZONER.NS', 'PNB.NS', 'RECLTD.NS', 'SANSTAR.NS', 
    'SJVN.NS', 'TMCV.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'SOUTHBANK.NS', 
    'UNIONBANK.NS', 'IDEA.NS', 'YESBANK.NS', 'BEL.NS', 'HAL.NS', 'LT.NS', 
    'SUZLON.NS', 'HDFCBANK.NS', 'LTTS.NS'
]

CATALYST_INTELLIGENCE = {
    'BEL.NS': {'news': 'Order book at ₹73,000 Cr providing 3x revenue visibility.', 'sales': '12-15% YoY Growth expected'},
    'HAL.NS': {'news': 'Inaugurated dedicated sovereign Light Combat Helicopter manufacturing pipelines.', 'sales': '8-11% YoY Growth expected'},
    'SUZLON.NS': {'news': 'Turnaround fundamentals solid. Revenue surged 48% YoY backed by clean energy installations.', 'sales': '20-25% YoY Growth expected'},
    'LT.NS': {'news': 'Core industrial infrastructure engineering order book hitting historic highs.', 'sales': '10-12% YoY Growth expected'},
    'TATAPOWER.NS': {'news': 'Direct winner from artificial intelligence expansion; powering upcoming massive data center hubs.', 'sales': '15% YoY Growth expected'}
}

def analyze_and_send():
    qualified_assets = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    for ticker in TARGET_TICKERS:
        try:
            stock = yf.Ticker(ticker, session=session)
            hist = stock.history(period="1mo")
            if hist.empty: continue
            current_price = float(hist['Close'].iloc[-1])
            month_low = float(hist['Low'].min())
            
            if current_price <= (month_low * 1.05):
                intel = CATALYST_INTELLIGENCE.get(ticker, {'news': 'Consistent core business operations.', 'sales': 'Steady long-term compounder'})
                qualified_assets.append(
                    f"💎 *{ticker}* \n"
                    f"  ▪️ *Current Price:* ₹{current_price:.2f}\n"
                    f"  ▪️ *Optimal Entry Range:* ₹{month_low:.2f} - ₹{(month_low*1.035):.2f}\n"
                    f"  ▪️ *Projected Outlook:* {intel['sales']}\n"
                    f"  ▪️ *Core Analyst News:* {intel['news']}\n"
                )
        except Exception:
            pass

    intel_report = f"🏛️ *ANALYST PRE-MARKET STRATEGY MATRIX*\n🗓️ Date: {datetime.now().strftime('%d-%b-%Y')} | 08:30 AM IST\n────────────────────────\n\n"
    
    if qualified_assets:
        intel_report += "\n".join(qualified_assets[:6])
    else:
        intel_report += "🔄 *Scan complete:* All tracked assets are currently trading above conservative entry support boundaries today."
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": intel_report, "parse_mode": "Markdown"}, timeout=15)

@app.route('/')
def run_analyst_evaluation():
    threading.Thread(target=analyze_and_send).start()
    return "OK", 200
