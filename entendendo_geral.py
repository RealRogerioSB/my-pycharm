# %%
# sem asyncio
import time
from timeit import timeit


def brew_coffee():
    print("Start brew_coffee()")
    time.sleep(3)
    print("End brew_coffee()")
    return "Coffee ready"


def toast_bagel():
    print("Start toast_bagel()")
    time.sleep(3)
    print("End toast_bagel()")
    return "Bagel toasted"


def main():
    start_time = time.time()

    result_coffee = brew_coffee()
    result_bagel = toast_bagel()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nResult of brewCoffee: {result_coffee}")
    print(f"Result of toastBagel: {result_bagel}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()

# %%
# com asyncio
import asyncio


async def brew_coffee():
    print("Start brew_coffee()")
    await asyncio.sleep(3)
    print("End brewCoffee()")
    return "Coffee ready!"


async def toast_bagel():
    print("Start toastBagel()")
    await asyncio.sleep(3)
    print("End toastBagel()")
    return "Bagel toasted!"


async def main():
    start_time = time.time()

    batch = asyncio.gather(brew_coffee(), toast_bagel())  # coroutine object
    result_coffee, result_bagel = await batch

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nResult of brew_coffee: {result_coffee}")
    print(f"Result of toast_bagel: {result_bagel}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())

# %%
# Assistente Pessoal
# from gtts import gTTS
# import speech_recognition as sr
# from playsound import playsound
# from requests import get
# from bs4 import BeautifulSoup
# import webbrowser as browser
# from paho.mqtt import publish

# CONFIGURAÇÕES
# hotword = "rose"

# with open("./db/rosie-python-assistente-fe02a8d39c53.json") as credenciais_google:
#     credenciais_google = credenciais_google.read()

# LISTAGEM DOS COMANDOS
# NOTÍCIAS.................... Últimas notícias
# TOCA <NOME DO ÁLBUM>........ Reproduz o álbum no spotify player web
# TEMPO AGORA................. Informações sobre temperatura e condição Climática
# TEMPERATURA HOJE............ Informações sobre mínima e máxima
# LIGA/DESATIVA BUNKER........ Controla iluminação do escritório


# FUNÇÕES PRINCIPAIS
# def monitora_audio():
#     microfone = sr.Recognizer()
#
#     with sr.Microphone() as source:
#         while True:
#             print("Aguardando o Comando:")
#             audio = microfone.listen(source)
#
#             try:
#                 trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language="pt-BR")
#                 trigger = trigger.lower()
#
#                 if hotword in trigger:
#                     print("COMANDO: ", trigger)
#                     responde("feedback")
#                     executa_comandos(trigger)
#                     break
#
#             except sr.UnknownValueError:
#                 print("Google não entendeu o áudio.")
#
#             except sr.RequestError as e:
#                 print("Não podia requerer resultados do serviço do Google Cloud Speech; {0}".format(e))
#
#     return trigger


# def responde(arquivo):
#     playsound("./src/" + arquivo + ".mp3")


# def cria_audio(mensagem):
#     tts = gTTS(mensagem, lang="pt-br")
#     tts.save("./src/mensagem.mp3")
#     print("ROSIE: ", mensagem)
#     playsound("./src/mensagem.mp3")


# def executa_comandos(trigger):
#     if "notícias" in trigger:
#         ultimas_noticias()
#     elif "toca" in trigger and "bee gees" in trigger:
#         playlists("bee_gees")
#     elif "toca" in trigger and "taylor davis" in trigger:
#         playlists("taylor_davis")
#     elif "tempo agora" in trigger:
#         previsao_tempo(tempo=True)
#     elif "temperatura hoje" in trigger:
#         previsao_tempo(minmax=True)
#     elif "liga o bunker" in trigger:
#         publica_mqtt("office/iluminacao/status", "1")
#     elif "desativa o bunker" in trigger:
#         publica_mqtt("office/iluminacao/status", "0")
#     else:
#         mensagem = trigger.strip(hotword)
#         cria_audio(mensagem)
#         print("C. INVÁLIDO", mensagem)
#         responde("comando_invalido")


# FUNÇÕES COMANDOS
# def ultimas_noticias():
#     site = get("https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt")
#     noticias = BeautifulSoup(site.text, "html.parser")
#     for item in noticias.findAll("item")[:2]:
#         mensagem = item.title.text
#         cria_audio(mensagem)


# def playlists(album):
#     if album == "bee_gees":
#         browser.open("https://open.spotify.com/track/33ALuUDfftTs2NEszyvJRm")
#     elif album == "taylor_davis":
#         browser.open("https://open.spotify.com/track/3MKep4BfEwSlAHuFJrA9aV")


# def previsao_tempo(tempo=False, minmax=False):
#     site = get("http://api.openweathermap.org/data/2.5/weather?id=3451190&APPID=111111111111111&units=metric&lang=pt")
#     clima = site.json()
#
#     temperatura = clima["main"]["temp"]
#     minima = clima["main"]["temp_min"]
#     maxima = clima["main"]["temp_max"]
#     descricao = clima["weather"][0]["description"]
#
#     if tempo:
#         mensagem = f"No momento fazem {temperatura} graus com: {descricao}."
#     elif minmax:
#         mensagem = f"Mínima de {minima} e máxima de {maxima} graus."
#
#     cria_audio(mensagem)


# def publica_mqtt(topic, payload):
#     publish.single(topic, payload=payload, qos=1, retain=True, hostname="m10.cloudmqtt.com", port=12892,
#                    client_id="rosie", auth={"username": "xxxxxxxx", "password": "xxxxxxxx"})
#
#     mensagem = "Bunker Ligado!" if payload == "1" else "Bunker Desligado!"
#
#     cria_audio(mensagem)


# def main():
#     while True:
#         monitora_audio()


# if __name__ == "__main__":
#     main()

# %%
### Pirâmide com base de estrelas
num = int(input("Entra o número de linhas: "))

row = 0

while num > row:
    space = num - row - 1
    while space > 0:
        print(end=" ")
        space -= 1
    star = row + 1
    while star > 0:
        print("*", end=" ")
        star -= 1
    row += 1
    print()

# %%
### Pirâmide com base de números
num = int(input("Entra o número de linhas: "))

for i in range(1, num + 1):
    for j in range(1, num - i + 1):
        print(end=" ")
    for j in range(i, 0, -1):
        print(j, end="")
    for j in range(2, i + 1):
        print(j, end="")
    print()

# %%
# Downloader YouTube
# from pytube import YouTube

# video = YouTube("https://www.youtube.com/watch?v=D_25fG8ipi8")
# stream = video.streams.first()
# stream = video.streams.get_highest_resolution()
# stream.download("./img/")

# %%
# Imagem Pillow (converter colorido em preto e branco)
from PIL import Image

img = Image.open("./img/grafico.png")
black_white = img.convert("L")
black_white.save("./img/new_grafico.png")
black_white.show()

# %%
# Tradutor de Texto
# !pip install translate
# from translate import Translator

# entra no site https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes e pega o código da coluna "639-1"
# s = Translator(from_lang="en", to_lang="pt")
# pode ser assim: s = Translator(to_lang="portuguese"),
# pois ao omitir o parâmetro "from_lang" passa a ser autodetect
# res = s.translate("Hello, Guys!")
# print(res)

# %%
# QRCode
# pip install qrcode
# import qrcode

# qr = qr_code.QRCode(
#     version=1,
#     error_correction=qr_code.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4
# )

# adiciona o texto ao QR Code
# qr.add_data("Texto que você quer adicionar ao QR Code")

# gera o QR Code
# qr.make(fit=True)

# cria um objeto de imagem a partir do QR Code
# img = qr.make_image(fill_color="black", back_color="white")

# salva a imagem em um arquivo PNG
# img.save("./img/qr_code.png")

# %%
# SpeedTest
# import speedtest

# teste = speedtest.Speedtest()
# down_ = teste.download()
# up_ = teste.upload()
# ping_ = speedtest.results.ping()
# print(f"Download: {down_ / 10**6:,.2f}MB.")
# print(f"Upload: {up_ / 10**6:,.2f}MB.")
# print(f"Ping: {ping_:,.2f}ms.")

# %%
# PDF merger
import os
import PyPDF2

merger = PyPDF2.PdfMerger(strict=False)

arquivos = os.listdir("doc")

for arquivo in arquivos:
    if arquivo.endswith(".pdf"):
        merger.append(f"doc/{arquivo}")

merger.write("./doc/hashProgramação.pdf")


# %%
# Captura de Tela
# import pyautogui

# captura a tela inteira
# screenshot = pyautogui.screenshot()
# screenshot.save("./img/screenshot.png")

# captura a tela específica
# screenshot = pyautogui.screenshot(region=(0, 0, 500, 300))
# screenshot.save("./img/screenshot_2.png")

# %%
# Conversão de áudio em texto
# pip install SpeechRecognition
# import speech_recognition as sr

# r = sr.Recognizer()

# # inicializa o microfone
# with r.Microfone() as source:
#     print("Diga alguma coisa:")
#     audio = r.listen(source)

# try:
#     text = r.recognize_google(audio, language="pt-BR")
#     print(f"Você disse: {text}")
# except sr.UnknownValueError:
#     print("Não entendi o que você disse.")
# except sr.RequestError as e:
#     print(f"Erro de requisição: {e}")

# %%
# Tocador de Música
# import pygame

# # inicializa o pygame
# pygame.init()

# # carrega a música
# pygame.mixer.music.load("./src/minhamusica.mp3")

# # toca a música
# pygame.mixer.music.play()

# # espera até a música termine
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)

# # encerra a música
# pygame.quit()

# %%
# Atualizações sobre o Clima
# pip install pyowm
# import pyowm

# inicializa o OWM (OpenWeatherMap) com a sua chave de API
# owm = pyowm.OWM("Sua_Chave_De_API_Aqui")

# define a cidade que você quer obter o clima
# city = "São Paulo, BR"

# obtém as informações sobre o clima
# weather = owm.weather_at_place(city).get_weather()

# imprime a temperatura atual em graus celsius
# temperature = weather.get_temperature("celsius")["temp"]
# print(f"A temperatura atual em {city} é de {temperature:.1f} ºC.")

# %%
# Encurtador URL
# pip install pyshorteners
# import pyshorteners

# s = pyshorteners.ShortEner()

# define o URL que você quer encurtar
# url = "https://www.meu_url.com.br"

# encurta o URL usando o serviço TinyURL
# short_url = s.tinyurl.short(url)

# print(short_url)

# %%
# URLOPEN
# Versão que usa tentativa/exceção para imprimir
# uma mensagem de erro se o urlopen falhar.
def wget2(url_):
    from urllib.request import urlopen

    try:
        ufile = urlopen(url_)
        if ufile.info().get_content_type() == "text/html":
            print(ufile.read())
    except IOError:
        print(f"Problema de leitura URL: {url_}")


wget2("https://www.youtube.com/watch?v=eguv8wv3jN0")

# %%
a = 0b1010  # Binary Literals
b = 100  # Decimal Literal
c = 0o310  # Octal Literal
d = 0x12c  # Hexadecimal Literal

# Float Literal
float_1 = 10.5
float_2 = 1.5e2

# Complex Literal
x = 3.14j

print(a, b, c, d)
print(float_1, float_2)
print(x, x.imag, x.real)

# %%
strings = "Este é Python"
char = "C"
multiline_str = """Isto é um string
 multilinha com mais
  do que uma linha."""
unicod = u"\u00dcnic\u00f6de"
raw_str = r"raw \n string"
cifrao = "\u0024"
aMaiusculo = "\u0041"
tique = "\u2705"
quatro = "\u0034"
heart = "\u1F499"
covid = "\u1F9A0"
hiragana = "\u3041"

print(strings)
print(char)
print(multiline_str)
print(unicod)
print(raw_str)
print(cifrao)
print(aMaiusculo)
print(tique)
print(quatro)
print(heart)
print(covid)
print(hiragana)

# %%
# comparando desempenho com listas (array e list)
import numpy as np

np_array = np.arange(int(1e6))

for _ in np.arange(100): np_array *= 2

py_list = list(range(int(1e6)))

for _ in range(100): py_list = [x * 2 for x in py_list]

# %%
# só serve para Notebook Jupyter
from time import sleep

print("Contagem Regressiva Iniciada.")

for i in range(10, -1, -1):
    print(f"{i:2d}", end="\r")
    sleep(1)
else:
    print("Contagem Regressiva Terminada.")

# %%
drink = "Disponível"
food = None


def menu(x_):
    if x_ == drink:
        print(drink)
    else:
        print(food)


menu(drink)
menu(food)


# %%
def outer_function():
    a = 20

    def inner_function():
        a = 30
        print("a =", a)

    inner_function()
    print("a =", a)


a = 10
outer_function()
print("a =", a)


# %%
def outer_function():
    global a
    a = 20

    def inner_function():
        global a
        a = 30
        print("a =", a)

    inner_function()
    print("a =", a)


a = 10
outer_function()
print("a =", a)


# %%
def outer():
    x = "local"

    def inner():
        nonlocal x
        x = "nonlocal"
        print("Dentro:", x)

    inner()
    print("Fora:", x)


outer()

# %%
c = 0


def add():
    global c
    c += 2
    print("Dentro add():", c)


add()
print("Em principal:", c)

# %%
print("Dê-me 2 números, e os dividirei.")
print("Toque a tecla 'q' para sair.")

while True:
    first_number = input("\nEscolha o 1º número: ")
    if first_number == "q":
        break
    second_number = input("Escolha o 2º número: ")
    if second_number == "q":
        break
    try:
        answer = int(first_number) / int(second_number)
    except ZeroDivisionError:
        print("Você não pode dividir por zero!")
    except ValueError:
        print("Só deve colocar caracteres numéricos.")
    else:
        print("A divisão dos 2 números é", answer)

# %%
quit_flag = 0

match quit_flag:
    case True:
        print("Desistindo...")
    case False:
        print("O sistema está on.")
    case _:
        print("Valor booleano não foi passado.")

# %%
# Permutações com ‘string’
import itertools

for p in itertools.permutations("ABCD"):
    print(p)


# %%
def media(listagem):
    assert len(listagem) != 0, "A lista está vazia..."
    return sum(listagem) / len(listagem)


a = [55, 88, 78, 90, 79]
b = []

print(f"A média da lista A é {media(a)}.")

try:
    print(f"A média da lista B é {media(b)}.")
except AssertionError as err:
    print(err)

# %%
help(len)

# %%
texto: str = input("Escreva algo: ")
print()
print(texto or "Vazio...")
print(f"{texto} -> {type(texto)}")
print()
print(texto or None or False or 0 or "Você não escreveu nada.")
print()
texto = texto or None
print(f"{texto} -> {type(texto)}")
print()
if texto:
    print("Escreveu algo.")
else:
    print("Não escreveu nada.")
print(f"{texto} -> {type(texto)}")
print()

a, b, c, d, e, f, g = "", None, False, [], {}, 22, "Giovana"

var = a or b or c or d or e or f or g
print(var)

# %%
# determina saber qual encode configura o arquivo binário
# import chardet

# with open("./src/aluguel.csv", "rb") as filename:
#     print(chardet.detect(filename.read()))

# %%
import numpy as np


def acumulador():
    for yy in np.arange(100):
        yield yy


print(list(acumulador()))


# %%
def timer(fun):
    def decor(*args, **kwargs):
        start = time.perf_counter()
        fun(*args, **kwargs)
        end = time.perf_counter()
        return f"Esta função demorou {end - start:.9f} segundos..."

    return decor


@timer
def fun1():
    soma = 0
    for xx in range(1000):
        soma += xx * 4
    print(soma)


fun1()

# %%
import sys
from functools import wraps
from time import perf_counter


def fast(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper


@fast
def fibonacci(n: int) -> int:
    if n <= 1:
        return n

    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    sys.setrecursionlimit(int(1e6))

    x: int = 1000

    start_time: float = perf_counter()
    result: int = fibonacci(x)
    end_time: float = perf_counter()

    print(f"Fibonacci({x}) = {result}\nTempo de execução: {end_time - start_time:.8f} segundos")

# %%
# import wget

# link = ""
# wget.download(link, "busca_pdf.pdf")

# %%
# import cv2
# import numpy as np
# import pyautogui

# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# tela_larg, tela_altu = pyautogui.size()
# saida = cv32.VideoWriter_fourcc("screencast.avi", fourcc, 20.0, (tela_larg, tela_altu))

# while True:
#     captura = pyautogui.screenshot()
#     frame = cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR)
#     saida.write(frame)

# if cv2.waitKey(1) == ord("q"):
#     break

# saida.release()
# cv2.destroyAllWindows()
