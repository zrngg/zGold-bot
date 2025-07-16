import requests
import time
from datetime import datetime
import pytz
import telebot

# 🔑 Your credentials
API_KEY = "60d2debf31ec6952e774e3ca53d863fd60d2debf"
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ✅ Get silver price per ounce
def get_silver_price():
    try:
        url = "https://goldpricez.com/api/rates/currency/usd/measure/ounce/type/silver"
        headers = {"X-API-KEY": API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return float(data.get("ounce_price_usd", 0))
    except Exception as e:
        print("❌ Error fetching silver price:", e)
        return 0

# ✅ Send only silver kilo price
def send_silver_kilo():
    silver_oz_price = get_silver_price()
    if silver_oz_price == 0:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch silver price.")
        return

    # Convert ounce to gram, then to kilo
    oz_to_gram = 31.1
    silver_per_gram = silver_oz_price / oz_to_gram
    silver_kilo = silver_per_gram * 1000

    # Time in GMT+3
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    # Message
    message = (
        f"{now} (GMT+3)\n"
        f"====================\n"
        f"⚪ Silver Price\n"
        f"1 Kilogram = ${silver_kilo:,.2f}\n"
        f"===================="
    )

    bot.send_message(CHANNEL_USERNAME, message)
    print("✅ Silver price sent!")

# 🔁 Run every 30 minutes
if __name__ == "__main__":
    while True:
        send_silver_kilo()
        time.sleep(1800)
