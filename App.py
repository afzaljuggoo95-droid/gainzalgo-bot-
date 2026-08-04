from flask import Flask, request
import requests, datetime, pytz, os

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def is_trading_hours():
    tz = pytz.timezone('Indian/Mauritius')
    now = datetime.datetime.now(tz)
    return 14 <= now.hour < 22

@app.route('/webhook', methods=['POST'])
def webhook():
    if not is_trading_hours():
        return "Hors heures 14h-22h Maurice", 200
        
    data = request.json
    price = float(data['price'])
    sl_pips = 2.5  
    tp_pips = 5.0
    
    if data['action'] == "BUY":
        sl = round(price - sl_pips, 2)
        tp = round(price + tp_pips, 2)
        emoji = "🟢"
    else:
        sl = round(price + sl_pips, 2)  
        tp = round(price - tp_pips, 2)
        emoji = "🔴"
    
    msg = f"""{emoji} GAINZALGO V2 ALPHA {emoji}
{data['action']} {data['symbol']} {data['timeframe']}
Prix: {price}
SL: {sl} | TP: {tp}
Heure: {datetime.datetime.now(pytz.timezone('Indian/Mauritius')).strftime('%H:%M')} Maurice"""
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": msg})
    return "OK", 200
