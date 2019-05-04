import requests
import telebot
import matplotlib.pyplot as plt
import urllib3

TOKEN = '813289742:AAEOgy6HS9waaaGS0iF3ftpk3h8CmucC4MY'

bot = telebot.TeleBot(TOKEN)

e1 = plt.imread('Perks/e1.png')
e2 = plt.imread('Perks/e2.png')
tmp = 'Perks/tmp.png'

session = requests.Session()
session.auth = ('RO', 'just4reading')
session.verify = False
urllib3.disable_warnings()


@bot.message_handler(commands=['start', 'help', 'show'])
def main_commands(message):
    if "/start" in message.text:
        bot.send_message(message.chat.id,text="Hi, i am UNIT Factory finder:)\nSimply type mac address or xlogin for find someone.\n/show - for see connected devices.")
    if "/help" in message.text:
        bot.send_message(message.chat.id,text="Simply type mac address or xlogin for find someone.\n/show - for see connected devices.")
    if "/show" in message.text:
        f = plt.figure(figsize=(5, 5), dpi=500)
        plt.xticks([])
        plt.yticks([])
        plt.axis('off')
        a = f.add_subplot(211, title='First floor')
        f.gca().axes.get_yaxis().set_visible(False)
        f.gca().axes.get_xaxis().set_visible(False)
        b = f.add_subplot(212, title='Second floor')
        a.imshow(e1)
        b.imshow(e2)
        f.gca().axes.get_yaxis().set_visible(False)
        f.gca().axes.get_xaxis().set_visible(False)

        response = session.get('https://cisco-cmx.unit.ua/api/location/v2/clients/')
        data = response.json()
        connected = "UNIT Factory(student):\n"
        for mac in data:
            if mac['macAddress']:
                if mac['userName']:
                    connected += mac['macAddress'] + "\t\t\t" + mac['userName'] + '\n'
                if '1st_Floor' in mac['mapInfo']['mapHierarchyString']:
                    a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=1)
                    a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=3)
                else:
                    b.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=1)
                    b.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=3)
        f.savefig(tmp)
        image = open(tmp, 'rb')
        bot.send_message(message.chat.id, text=connected)
        bot.send_photo(message.chat.id, image)


@bot.message_handler(content_types=['text'])
def echo_digits(message):
    response = session.get('https://cisco-cmx.unit.ua/api/location/v2/clients/')
    data = response.json()
    key = 1
    for mac in data:
        if (message.text in mac['macAddress'] or message.text in mac['userName']) and message.text:
            key = 0
            f = plt.figure(figsize=(5, 5), dpi=500)
            if '1st_Floor' in mac['mapInfo']['mapHierarchyString']:
                a = f.add_subplot(111, title='First floor')
                a.imshow(e1, extent=[0, 1550, 770, 0])
            else:
                a = f.add_subplot(111, title='Second floor')
                a.imshow(e2, extent=[0, 1550, 770, 0])
            f.gca().axes.get_yaxis().set_visible(False)
            f.gca().axes.get_xaxis().set_visible(False)
            a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=4)
            a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=4)
            f.savefig(tmp)
            image = open(tmp, 'rb')
            try:
                bot.send_photo(message.chat.id, image)
            except:
                pass
            break
    if key:
        bot.send_message(message.chat.id, text="Not connected(")

print ("Bot status is active.\nFollow: https://t.me/unit_factory_finder_bot")
bot.polling(timeout=60)

