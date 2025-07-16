import requests
import time
from datetime import datetime
import pytz
import telebot

# Telegram credentials
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

RATES_API_URL = 'https://data-asg.goldprice.org/dbXRates/USD'

def fetch_prices():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(RATES_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        prices = {}
        for item in data.get('items', []):
            currency = item['curr']
            gold_oz = item.get('xauPrice')
            silver_oz = item.get('xagPrice')

            # Convert ounces to grams
            OZ_TO_GRAM = 31.1035
            gold_g = gold_oz / OZ_TO_GRAM if gold_oz else None
            silver_g = silver_oz / OZ_TO_GRAM if silver_oz else None

            prices[currency] = {
                'gold_oz': round(gold_oz, 2) if gold_oz else None,
                'gold_g': round(gold_g, 2) if gold_g else None,
                'silver_oz': round(silver_oz, 2) if silver_oz else None,
                'silver_g': round(silver_g, 2) if silver_g else None,
            }
        return prices

    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

def send_silver_kilo():
    prices = fetch_prices()
    if not prices or 'USD' not in prices:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch silver price.")
        print("❌ Couldn't fetch silver price.")
        return

    silver_per_gram = prices['USD']['silver_g']
    if not silver_per_gram:
        bot.send_message(CHANNEL_USERNAME, "❌ Silver price data unavailable.")
        print("❌ Silver price data unavailable.")
        return

    silver_kilo = silver_per_gram * 1000

    # Time in GMT+3
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    message = (
        f"{now} (GMT+3)\n"
        f"====================\n"
        f"⚪ Silver Price\n"
        f"1 Kilogram = ${silver_kilo:,.2f}\n"
        f"===================="
    )

    bot.send_message(CHANNEL_USERNAME, message)
    print("✅ Silver price sent!")

if __name__ == "__main__":
    while True:
        send_silver_kilo()
        time.sleep(1800)  # 30 minutes
