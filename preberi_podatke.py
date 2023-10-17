import re
import os
import requests
import csv
import json
import traceback

seznam_gorovij = "https://www.hribi.net/gorovja" 
hribovja_directory = 'podatki'
page_filename = 'page'

def url_to_string (url): #Naredi niz iz url-ja.
    try:
      vsebina = requests.get(url)
      if vsebina.status_code == 200:
         return vsebina.text
      else:
        raise  ValueError(f"Napaka: {vsebina.status_code}")
    except:
        return "Napaka: ni šlo."

def save_string_to_file(text, mapa, datoteka): #Shrani niz v datoteko filename v mapi directory.
    os.makedirs(mapa, exist_ok=True)
    path = os.path.join(mapa, datoteka)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def url_to_file(url, mapa, datoteka): #Združi prejšnji funkciji za preprostejšo uporabo.
    html = url_to_string(url)
    save_string_to_file(url, mapa, datoteka)
    return None

url_to_file(seznam_gorovij, hribovja_directory, page_filename)