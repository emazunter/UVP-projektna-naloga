import re
import os
import requests
import csv
import json
import traceback

seznam_gorovij = 'https://www.hribi.net/gorovja'
hribovja_directory = 'podatki'
seznam_gorovij_dat = 'seznam-gorovij'

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

#Znotraj datoteke seznama najdemo url-je posameznih gora:
def ustvari_linke(datoteka):
    vsebina = file_content(datoteka)
    vzorec = "/gorovje/.*/\d+"
    seznam = []
    match_sez = re.findall(vzorec, vsebina)
    for koncnica_urlja in match_sez:
        cel_url = 'https://www.hribi.net' + koncnica_urlja
        seznam.append(cel_url)
    return seznam
#Znotraj datoteke seznama najdemo url-je posameznih gora.

#seznam_pravi = ustvari_linke(seznam_gorovij_dat)
#Ustvari pomožni seznam linkov.

def ustvari_datoteke(seznam_linkov):
    i = 1
    for link in seznam_linkov:
        url_to_file(link, hribovja_directory, f"hribovje-{i}.txt")
        i += 1
#Ustvari datoteke iz seznama url-jev.

#ustvari_datoteke(seznam_pravi)
#Ustvari datoteke s seznami gora.
