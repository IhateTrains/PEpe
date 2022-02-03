import discord

import pytesseract
from PIL import Image
from pepeToken import token
from Topic import Topic
from databases_manager import DatabseManager
client = discord.Client()

DBM = DatabseManager()
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#dioda2 = Topic('dioda2')
#tranzystor1 = Topic('tranzystor1')
#tranzystor2 = Topic('tranzystor2')
#wzmacniacze1 = Topic('wzmacniacze1')
#uklady1 = Topic('uklady1')

#topics = [dioda2, tranzystor1, tranzystor2, wzmacniacze1, uklady1]
flag = 0
def containsOneImageAttachment(message):
    if len(message.attachments) == 1 and message.attachments[0].width > 0:
        return True
    return False
DBM.load_databases()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!dodaj") and message.author.guild_permissions.administrator:
        new_name = message.content.strip().replace('!dodaj ', '').lower()
        DBM.add_to_database(name=new_name)
        DBM.load_databases()
        return
    message_start = message.content.split(" ")[0]
    print(f'message start: {message_start}')
    if message.content.startswith("!bazydanych"):
        print(DBM.get_databases())
    for topic in DBM.get_topics(message_start):
        screens = topic.get_screens()
        if len(message.content) > len(topic.name)+1:
            query = message.content.strip().replace(f'{message_start} ', '').lower()
            found_list = []
            for screen in screens:
                if screen.content.find(query) != -1:
                    found_list.append(screen.link)
            if len(found_list)> 0:
                for found in found_list:
                    await message.channel.send(found)
            else:

                await message.channel.send("Niczego nie znalazłem Sadge")
        else:
            if containsOneImageAttachment(message) and flag == 0:
                file = message.attachments[0]
                await file.save('image.png')
                ocrResult = pytesseract.image_to_string(Image.open('image.png'), lang='pol').lower().replace('\n', ' ')
                image_link = file.url
                topic.add_to_database(ocrResult, image_link)
client.run(token)
