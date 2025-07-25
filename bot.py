# Minor update to trigger Railway deploy
import telebot
import os
from routeros_api import RouterOsApiPool

BOT_TOKEN = os.getenv("BOT_TOKEN")
MTK_HOST = os.getenv("MTK_HOST")
MTK_USER = os.getenv("MTK_USER")
MTK_PASS = os.getenv("MTK_PASS")

bot = telebot.TeleBot(BOT_TOKEN)

def connect_to_mikrotik():
    api_pool = RouterOsApiPool(MTK_HOST, username=MTK_USER, password=MTK_PASS, plaintext_login=True)
    return api_pool.get_api()

@bot.message_handler(commands=['reset'])
def reset_hotspot_users(message):
    try:
        api = connect_to_mikrotik()
        hotspot_user = api.get_resource('/ip/hotspot/user')
        active_user = api.get_resource('/ip/hotspot/active')

        users = hotspot_user.get()
        actives = active_user.get()

        for user in users:
            hotspot_user.remove(id=user['.id'])

        for active in actives:
            active_user.remove(id=active['.id'])

        bot.reply_to(message, "✅ সমস্ত হটস্পট ইউজার রিসেট করা হয়েছে।")
        api.pool.disconnect()
    except Exception as e:
        bot.reply_to(message, f"❌ ত্রুটি: {e}")

bot.polling(non_stop=True)
