#V komentarjih sem pisala, kaj naredi posamezna funkcija, dodala pa sem tudi kodo, 
#ki sem jo poganjala tekom izdelave projektne naloge.

import re
import os
import requests
import csv
import json
import traceback

seznam_gorovij = 'https://www.hribi.net/gorovja'
hribovja_directory = 'podatki'
seznam_gorovij_dat = 'seznam-gorovij.txt'

def url_to_string (url): 
    try:
      vsebina = requests.get(url)
      if vsebina.status_code == 200:
         return vsebina.text
      else:
        raise  ValueError(f"Napaka: {vsebina.status_code}")
    except:
        return "Napaka: ni šlo."
#Naredi niz iz url-ja.

def save_string_to_file(text, mapa, datoteka):
    os.makedirs(mapa, exist_ok=True)
    path = os.path.join(mapa, datoteka)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None
#Shrani niz v datoteko filename v mapi directory.

def url_to_file(url, mapa, datoteka): 
    html = url_to_string(url)
    save_string_to_file(html, mapa, datoteka)
    return None
#Združi prejšnji funkciji za preprostejšo uporabo.

#url_to_file(seznam_gorovij, hribovja_directory, seznam_gorovij_dat)
#Pretvori glavni seznam v datoteko.

def file_content (datoteka):
    with open(datoteka, encoding='utf-8') as dat:
        return dat.read()
#Vrne vsebino datoteke.

def ustvari_linke(datoteka, vzorec):
    vsebina = file_content(datoteka)
    seznam = []
    match_sez = re.findall(vzorec, vsebina)
    for koncnica_urlja in match_sez:
        cel_url = 'https://www.hribi.net' + koncnica_urlja
        seznam.append(cel_url)
    #print(seznam)
    return seznam
#Znotraj datoteke seznama najdemo url-je posameznih gora.

#seznam_pravi = ustvari_linke(seznam_gorovij_dat, "/gorovje/.*/\d+")
#Ustvari pomožni seznam linkov.

def ustvari_datoteke(seznam_linkov):
    i = 1
    for link in seznam_linkov:
        url_to_file(link, hribovja_directory, f"hribovje-{i}.txt")
        i += 1
#Ustvari datoteke iz seznama url-jev.


#ustvari_datoteke(seznam_pravi)

#Ustvari datoteke s seznami gora.


# for i in range (1, 11):
#     mapa = f'hribovje {i}'
#     parent_mapa = 'podatki'
#     path = os.path.join(parent_mapa, mapa)
#     os.mkdir(path)

#Ustvari mape za posamezna gorovja.


# for i in range(1, 11):
#     datoteka = f'podatki/hribovje-{i}.txt'
#     seznam = ustvari_linke(datoteka, "/gora/.*?/\d*?/\d*")
#     indeks = 1
#     for link in seznam:
#         url_to_file(link, f"podatki/hribovje {i}", f"hrib {indeks}")
#         indeks += 1

#Iz linkov za posamezna gorovja ustvarimo še datoteke za posamezne gore. 
#Sedaj lahko začnemo urejati podatke v CSV obliko.
######################
vzorec_bloka = re.compile(
    r'<title>.*?'
    r'<div style="padding-top:10px;">',
    flags=re.DOTALL
)
#Iz strani vzamemo samo blok htmlja, v katerem so podatki, ki jih želimo.
# vzorec_gore = re.compile(
#     r'<title>.(?P<ime>.*?)</title>.*?'
#     r'<div class="g2"><b>Gorovje:</b> <a class="moder" href=".*?">(?P<gorovje>.*?)</a></div>.*?'
#     r'<div class="g2"><b>Višina:</b> (?P<višina>\d+)&nbsp;m</div>.*?'
#     r'<div class="g2"><b>Ogledov:</b>(?P<ogledi>\d+)</div>.*?'
#     r'<div class="g2"><b>Priljubljenost:</b> (?P<priljubljenost_procenti>\d+%)&nbsp;((?P<priljubljenost_mesto>\d+\.)&nbsp;mesto)</div>.*?'
#     r'<div class="g2"><b>Število slik:</b> <a class="moder" href="#slike">(?P<st_slik>\d+)</a></div>.*?'
#     r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(?P<st_poti>\d+)</a></div>.*?',
#     flags=re.DOTALL
#)
#Iz HTML-ja izločimo samo podatke, ki nas zanimajo.

vzorec_gore = re.compile(
    r'form.*?id=(?P<id>.*?)".*?'
    r'<h1>(?P<ime>.*?)<\/h1>.'
    r'*?Država:<\/b>.*?>'
    r'(?P<drzava>.*?)<.*?'
    r'Gorovje:<\/b>.*?>(?P<gorovje>.*?)<.*?'
    r'Višina:\D*(?P<visina>\d*).*?'
    r'<b>Vrsta:</b>(?P<vrsta>.*?)</div>.*?'
    r'<b>Priljubljenost:</b>.*?(?P<priljubljenost>\d*)%.*?'
    r'<table class="TPoti".*?</tr>\s*(?P<tabelapoti>.*?)\s*</table>',
    re.DOTALL
)

def izloci_podatke(blok):
    gora = vzorec_gore.search(blok)#.groupdict()
    print(gora)
    gora['višina'] = int(gora['višina'])
    gora['ogledi'] = int(gora['ogledi'])
    gora['st_slik'] = int(gora['st_slik'])
    gora['st_poti'] = int(gora['st_poti'])

with open('podatki/hribovje 1/hrib 1') as f:
    vsebina = f.read()

for blok in vzorec_bloka.finditer(vsebina):
    # print(blok.group(0))
     print(izloci_podatke(blok.group(0)))

