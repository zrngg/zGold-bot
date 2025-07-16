import requests
import telebot
import time
from datetime import datetime
import pytz

# ✅ Your real API keys
GOLDAPI_KEY = 'goldapi-ho4919md64h04o-io'  # replace with your GoldAPI.io key
TOKEN = '8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I'
CHANNEL_USERNAME = "@gold_dataaaa"

bot = telebot.TeleBot(TOKEN)

# ✅ Fetch gold price from GoldAPI.io
def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": GOLDAPI_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("GoldAPI Error:", response.status_code, response.text)
            return 0
        data = response.json()
        return float(data.get("price", 0))
    except Exception as e:
        print("Exception fetching gold:", e)
        return 0

# ✅ Fetch silver price from metals.live
def get_silver_price():
    try:
        url = "https://api.metals.live/v1/spot"
        response = requests.get(url)
        if response.status_code != 200:
            print("Silver API Error:", response.status_code, response.text)
            return 0
        data = response.json()[0]
        return float(data.get('silver', 0))
    except Exception as e:
        print("Exception fetching silver:", e)
        return 0

def main():
    tz = pytz.timezone("Etc/GMT-3")
    oz_to_gram = 31.1

    while True:
        gold_price = get_gold_price()
        silver_price = get_silver_price()

        if gold_price == 0:
            bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch gold price.")
            time.sleep(1800)
            continue

        if silver_price == 0:
            bot.send_message(CHANNEL_USERNAME, "❌ Couldn't fetch silver price.")
            time.sleep(1800)
            continue

        now = datetime.now(tz).strftime("%d %B %Y | %H:%M")

        g999 = gold_price / oz_to_gram
        g995 = g999 * 0.995
        m21 = g999 * 0.875 * 5
        m18 = g999 * 0.750 * 5
        lira_dubai = g999 * 0.916 * 7.2
        g250 = g999 * 0.995 * 250
        g500 = g999 * 0.995 * 500
        g1000 = g999 * 0.995 * 1000

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

        bot.send_message(CHANNEL_USERNAME, message)
        print(f"Sent message at {now}")

        time.sleep(1800)  # Wait 30 minutes

if __name__ == "__main__":
    main()
