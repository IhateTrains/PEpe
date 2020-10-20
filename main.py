import discord
import pytesseract
from PIL import Image
import os
from pepeToken import *

client = discord.Client()

pytesseract.pytesseract.tesseract_cmd = r'E:\Users\Seweryn\AppData\Local\Tesseract-OCR\tesseract.exe'


def wczytajBaze():
    screeny = {}
    firstUsableId = 0
    try:
        baza = open('baza.txt', 'r')
        # read first usable ID
        firstUsableId = int(baza.readline())
        imagePairLines = baza.readlines()
        for line in imagePairLines:
            pozycja = line.rfind('; ')
            screeny[line[:pozycja]] = line[pozycja + 2:].strip()
        baza.close()
    except FileNotFoundError:
        print('Nie wczytano bazy')
    return firstUsableId, screeny


def zapiszBaze(firstUsableId, screeny):
    baza = open('baza.txt', 'w')
    # save first usable ID
    baza.write(str(firstUsableId) + '\n')
    for key in screeny.keys():
        baza.write(key + '; ' + screeny[key] + '\n')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def containsOneImageAttachment(message):
    if len(message.attachments) == 1 and message.attachments[0].width > 0:
        return True
    return False


@client.event
async def on_message(message):
    baza = wczytajBaze()
    screeny = baza[1]  # pary: tekst z OCR, nazwa obrazka
    firstUsableId = baza[0]

    if message.author == client.user:
        return

    if message.content.startswith('!pepe '):  # użytkownik prosi o pomoc
        query = message.content.strip().replace('!pepe ', '').lower()
        listaZnalezionych = []
        for key in screeny.keys():
            if key.find(query) != -1:
                listaZnalezionych.append(screeny[key])

        if len(listaZnalezionych) > 0:
            await message.channel.send('{.author.mention}, coś dla ciebie mam!'.format(message))
            for znaleziony in listaZnalezionych:
                await message.channel.send(file=discord.File(znaleziony))
        else:
            await message.channel.send('Niestety niczego nie znalazłem :(')

    else:
        if containsOneImageAttachment(message):
            # zapisz obrazek do OCR
            file = message.attachments[0]
            await file.save('obrazek.jpg')

            ocrResult = pytesseract.image_to_string(Image.open('obrazek.jpg'), lang='pol').lower().replace('\n', ' ')
            if ocrResult.find('dobra odpowiedź') != -1:
                nazwaObrazka = str(firstUsableId) + '.jpg'
                firstUsableId += 1
                if list(screeny.keys()).count(ocrResult) > 0:  # zadanie jest już w bazie
                    os.remove(screeny[ocrResult])
                await file.save(nazwaObrazka)
                screeny[ocrResult] = nazwaObrazka
                zapiszBaze(firstUsableId, screeny)
                await message.channel.send('Obrazek przyjęty, dziena byczq +1')


client.run(token)
