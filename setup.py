import sys

import telegram
from flask import Flask, request
import first_transition as ft

app = Flask(__name__)
bot = telegram.Bot(token='434221090:AAGIniGBERUTy6bTkPqQgZzP3UXkhU4eif8')
bus = ft.BusInfo()

def _set_webhook():
    status = bot.set_webhook('https://cbd9b717.ngrok.io/hook')
    if not status:
        print('Webhook setup failed')
        sys.exit(1)

@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        text = update.message.text

        if text.lower() == 'activate':
            bus.activate()
            res = 'activated'
        elif text.lower() == 'update':
            bus.update()
            res = bus.res
        elif u'從' in text and u'到' in text:
            bus.by_route(text)
            res = bus.res
        else:
            res = '使用方法： "路線"從"起站"到"下車站"'

        update.message.reply_text(res)
    return 'ok'

if __name__ == "__main__":
    _set_webhook()
    app.run()