import discord
import pytesseract
from PIL import Image
import os

# pepeToken.py should exist in the same dir as main.py, and contain a 'token' variable
# DO NOT SHARE YOUR TOKEN
from pepeToken import token

client = discord.Client()


def wczytajBaze():
    screeny = {}
    try:
        baza = open('baza.txt', 'r+')
        imagePairLines = baza.readlines()
        for line in imagePairLines:
            pozycja = line.rfind('; ')
            screeny[line[:pozycja]] = line[pozycja + 2:].strip()
        baza.close()
    except FileNotFoundError:
        print('Nie wczytano bazy')
    return screeny


def zapiszBaze(screeny):
    baza = open('baza.txt', 'w+')
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
    screeny = wczytajBaze()  # pary: tekst z OCR, link do obrazka

    if message.author == client.user:
        return

    # komenda !pepe
    if message.content.startswith('!pepe '):  # użytkownik prosi o pomoc
        query = message.content.strip().replace('!pepe ', '').lower()
        listaZnalezionych = []
        for key in screeny.keys():
            if key.find(query) != -1:
                listaZnalezionych.append(screeny[key])

        if len(listaZnalezionych) > 0:
            await message.channel.send('{.author.mention}, coś dla ciebie mam!'.format(message))
            for znaleziony in listaZnalezionych:
                await message.channel.send(znaleziony)
        else:
            await message.channel.send('Niestety niczego nie znalazłem :(')

    # komenda !pesize (wyświetl ilość tekstów w bazie)
    elif message.content.startswith('!pesize'):
        await message.channel.send('Rozmiar bazy: {}'.format(len(screeny)))

    elif message.content.startswith('!pehelp'):
        await message.channel.send('Moje komendy:\n'
                                   '\t**!pepe <fragment tekstu>** - zwróć screeny z danym fragmentem tekstu\n'
                                   '\t**!pesize** - wyświetl rozmiar bazy\n'
                                   '\t**!pehelp** - wyświetl pomoc\n')

    else:
        if containsOneImageAttachment(message):
            # zapisz obrazek do OCR
            file = message.attachments[0]
            await file.save('obrazek.png')

            ocrResult = pytesseract.image_to_string(Image.open('obrazek.png'), lang='pol').lower().replace('\n', ' ')
            linkDoObrazka = file.url
            if list(screeny.keys()).count(ocrResult) > 0:  # zadanie jest już w bazie
                await message.add_reaction('👌')
            else:
                screeny[ocrResult] = linkDoObrazka
                zapiszBaze(screeny)
                await message.add_reaction('❤')


client.run(token)
