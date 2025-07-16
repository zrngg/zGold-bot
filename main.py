import requests
import time
from datetime import datetime
import pytz
import telebot

TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
RATES_API_URL = 'https://data-asg.goldprice.org/dbXRates/USD'

def fetch_prices():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(RATES_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        if not items:
            return None
        return items[0]
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

def calculate_prices(gold_ounce_price, silver_ounce_price):
    if not gold_ounce_price or not silver_ounce_price:
        return None

    gram_gold_price = gold_ounce_price / 31.1
    gram_silver_price = silver_ounce_price / 31.1

    prices = {
        'Msqal 21K 875': gram_gold_price * 0.875 * 5,
        'Msqal 18K 875': gram_gold_price * 0.75 * 5,
        'Lira Dubai 22K 7.2g': gram_gold_price * 0.916 * 7.2,
        '250g 24K 995': gram_gold_price * 0.995 * 250,
        '500g 24K 995': gram_gold_price * 0.995 * 500,
        '1Kg 24K 995': gram_gold_price * 0.995 * 1000,
        'Silver 1Kg': gram_silver_price * 1000,
    }
    return prices

def send_prices():
    prices_data = fetch_prices()
    if not prices_data:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch prices.")
        print("❌ Couldn't fetch prices.")
        return

    gold_ounce_price = prices_data.get('xauPrice')
    silver_ounce_price = prices_data.get('xagPrice')

    if gold_ounce_price is None or silver_ounce_price is None:
        bot.send_message(CHANNEL_USERNAME, "❌ Gold or silver ounce price not available.")
        print("❌ Gold or silver ounce price not available.")
        return

    prices = calculate_prices(gold_ounce_price, silver_ounce_price)
    if not prices:
        bot.send_message(CHANNEL_USERNAME, "❌ Error calculating prices.")
        print("❌ Error calculating prices.")
        return

    # Time in GMT+3
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    message = (
        f"{now} (GMT+3)\n"
        "——————————————————\n"
        f"Gold Ounce Price: ${gold_ounce_price:,.2f}\n"
        "——————————————————\n"
        f"Msqal 21K = ${prices['Msqal 21K 875']:,.2f}\n"
        f"Msqal 18K = ${prices['Msqal 18K 875']:,.2f}\n"
        f"Dubai Lira 7.2g = ${prices['Lira Dubai 22K 7.2g']:,.2f}\n"
        "——————————————————\n"
        f"250g 995 = ${prices['250g 24K 995']:,.2f}\n"
        f"500g 995 = ${prices['500g 24K 995']:,.2f}\n"
        f"1Kg 995 = ${prices['1Kg 24K 995']:,.2f}\n"
        "——————————————————\n"
        f"Silver 1Kg = ${prices['Silver 1Kg']:,.2f}\n"
        "—————————"
    )

    bot.send_message(CHANNEL_USERNAME, message)
    print("✅ Gold and silver prices sent!")

if __name__ == "__main__":
    while True:
        send_prices()
        time.sleep(1800)  # 30 minutes
