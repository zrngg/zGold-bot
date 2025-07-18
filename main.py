import requests
from datetime import datetime
import pytz
import telebot
import time

# Configuration
TELEGRAM_TOKEN = "8084011114:AAGqCKTt-3HibbZU6ttBAg1PK9Xb3ZJHw7I"
CHANNEL_USERNAME = "@gold_dataaaa"
IMAGE_URL = "https://i.postimg.cc/cK2YKyZb/gold-price.jpg"  # Modified URL for better compatibility
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# [Keep all your existing API and calculation functions...]

def send_message():
    msg = generate_message()
    
    try:
        # First try to send image with caption (most users prefer this)
        bot.send_photo(
            CHANNEL_USERNAME,
            IMAGE_URL,
            caption=msg[:1024],  # Telegram has 1024 character limit for captions
            parse_mode='Markdown'
        )
        print("✅ Message with image sent successfully.")
    except Exception as img_error:
        print(f"❌ Image send failed: {img_error}")
        try:
            # Fallback 1: Send image and text as separate messages
            bot.send_photo(CHANNEL_USERNAME, IMAGE_URL)
            bot.send_message(
                CHANNEL_USERNAME,
                msg,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            print("✅ Sent image and text separately.")
        except Exception as separate_error:
            print(f"❌ Separate send failed: {separate_error}")
            try:
                # Final fallback: Text only with WhatsApp link
                bot.send_message(
                    CHANNEL_USERNAME,
                    msg,
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
                print("✅ Sent text message only.")
            except Exception as text_error:
                print(f"❌ Complete failure: {text_error}")

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
            time.sleep(60)  # Wait 1 minute before retrying after errors
