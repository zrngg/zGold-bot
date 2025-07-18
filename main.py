import requests
from datetime import datetime
import pytz
import telebot
import time

# Configuration
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"
IMAGE_URL = "https://postimg.cc/cK2YKyZb"  # Replace with your actual Imgur URL
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# [Keep all your existing API and calculation functions...]

def send_message():
    msg = generate_message()
    
    # First verify the image URL
    image_valid = False
    try:
        resp = requests.head(IMAGE_URL, timeout=5)
        image_valid = resp.status_code == 200
    except:
        image_valid = False
    
    if image_valid:
        try:
            # Try sending image with caption
            bot.send_photo(
                CHANNEL_USERNAME,
                IMAGE_URL,
                caption=msg[:1024],
                parse_mode='Markdown'
            )
            print("✅ Message with image sent successfully.")
            return
        except Exception as img_error:
            print(f"❌ Image send failed: {img_error}")
    
    # If image fails or is invalid, send text only
    try:
        bot.send_message(
            CHANNEL_USERNAME,
            msg,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        print("✅ Sent text message.")
    except Exception as text_error:
        print(f"❌ Failed to send message: {text_error}")

if __name__ == "__main__":
    print("🚀 Gold Price Bot Started")
    while True:
        try:
            send_message()
            time.sleep(300)  # 5 minute interval
        except KeyboardInterrupt:
            print("🛑 Bot stopped by user")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            time.sleep(60)
