import telebot
import os

TOKEN = os.getenv("7769917327:AAEdY6xTfU5ckItdlSWBJUR9wKT1G618v6w")
bot = telebot.TeleBot(TOKEN)

products = {
    "نوشابه": 40000,
    "نوشابه فانتا": 40000,
    "برنج": 1000000,
    "روغن": 450000
}

orders = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "سلام! به سوپرمارکت خوش اومدی. برای سفارش یکی از گزینه‌های زیر رو بفرست:\n\n"
    for item, price in products.items():
        text += f"{item} - {price} تومان\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text in products)
def handle_order(message):
    user_id = message.chat.id
    item = message.text
    price = products[item]

    if user_id not in orders:
        orders[user_id] = []
    orders[user_id].append((item, price))

    bot.send_message(user_id, f"{item} به سبد خریدت اضافه شد.\nبرای دیدن سفارشات، بنویس: سبد خرید")

@bot.message_handler(func=lambda message: message.text == "سبد خرید")
def show_cart(message):
    user_id = message.chat.id
    if user_id not in orders or not orders[user_id]:
        bot.send_message(user_id, "سبد خریدت خالیه.")
        return

    total = 0
    text = "سفارشاتت:\n"
    for item, price in orders[user_id]:
        text += f"- {item}: {price} تومان\n"
        total += price
    text += f"\nمجموع: {total} تومان"
    bot.send_message(user_id, text)

bot.infinity_polling()
