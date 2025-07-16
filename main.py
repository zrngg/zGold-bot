import requests
import telebot
import time
from datetime import datetime
import pytz

# ✅ Your real API keys
NINJAS_API_KEY = 'WC/OwCltjWPfDUqcCJZV9Q==10Sn12y1EVPalh2T'
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TOKEN)

# ✅ Fetch gold price from API-Ninjas
def get_gold_price():
    try:
        url = "https://api.api-ninjas.com/v1/commodities?name=gold"
        headers = { "X-Api-Key": NINJAS_API_KEY }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Gold Error:", response.status_code, response.text)
            return 0
        data = response.json()
        return float(data[0]['price'])
    except Exception as e:
        print("Exception fetching gold:", e)
        return 0

# ✅ Fetch silver from metals.live
def get_silver_price():
    try:
        url = "https://api.metals.live/v1/spot"
        response = requests.get(url)
        data = response.json()[0]
        return float(data['silver'])
    except Exception as e:
        print("Exception fetching silver:", e)
        return 0

# ✅ Main loop: sends price every 30 minutes
while True:
    gold_price = get_gold_price()
    silver_price = get_silver_price()

    if gold_price == 0:
        bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price.")
        time.sleep(1800)
        continue

    # Format time (Iraq GMT+3)
    tz = pytz.timezone("Etc/GMT-3")
    now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

    # Calculations
    oz_to_gram = 31.1
    g999 = gold_price / oz_to_gram
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
        f"Gold Ounce Price: ${gold_price:,.2f}\n"
        f"Silver Ounce Price: ${silver_price:,.2f}\n"
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

    # ✅ Send to Telegram channel
    bot.send_message(CHANNEL_USERNAME, message)

    # Wait 30 minutes
    time.sleep(1800)
