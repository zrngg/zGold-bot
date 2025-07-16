import requests
import json
import time
from datetime import datetime
import pytz
import telebot

# 🔑 Set your credentials
API_KEY = "60d2debf31ec6952e774e3ca53d863fd60d2debf"
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"  # Your channel username

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ✅ Get gold price from GoldPricez
def get_gold_price():
    try:
        url = "https://goldpricez.com/api/rates/currency/usd/measure/ounce"
        headers = { "X-API-KEY": API_KEY }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # Double JSON parse
        parsed_string = response.json()
        data = json.loads(parsed_string)
        price = float(data.get("ounce_price_usd", 0))
        return price
    except Exception as e:
        print("❌ Error fetching gold price:", e)
        return 0

# ✅ Send message to Telegram
def send_gold_price():
    price = get_gold_price()
    if price == 0:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price.")
        return

    # Format timestamp (GMT+3)
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    # Calculations
    oz_to_gram = 31.1
    g999 = price / oz_to_gram
    g995 = g999 * 0.995
    m21 = g999 * 0.875 * 5
    m18 = g999 * 0.750 * 5
    lira_dubai = g999 * 0.916 * 7.2
    g250 = g999 * 0.995 * 250
    g500 = g999 * 0.995 * 500
    g1000 = g999 * 0.995 * 1000

    # Message
    message = (
        f"{now} (GMT+3)\n"
        f"——————————————————\n"
        f"Gold Ounce Price: ${price:,.2f}\n"
        f"——————————————————\n"
        f"Msqal 21K = ${m21:,.2f}\n"
        f"Msqal 18K = ${m18:,.2f}\n"
        f"Dubai Lira 7.2g = ${lira_dubai:,.2f}\n"
        f"——————————————————\n"
        f"250g 995 = ${g250:,.2f}\n"
        f"500g 995 = ${g500:,.2f}\n"
        f"1Kg 995 = ${g1000:,.2f}\n"
        f"—————————"
    )

    bot.send_message(CHANNEL_USERNAME, message)
    print("✅ Message sent!")

# 🔁 Loop every 30 mins
if __name__ == "__main__":
    while True:
        send_gold_price()
        time.sleep(1800)  # 30 minutes
