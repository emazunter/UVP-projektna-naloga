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
csv_dat = 'gore.csv'

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
vzorec_bloka = re.compile(
    r'<title>.*?'
    r'<div style="padding-top:10px;">',
    flags=re.DOTALL
)
#Iz strani vzamemo samo blok htmlja, v katerem so podatki, ki jih želimo.

vzorec_gore = re.compile(
    r'<div class="naslov1"><div style="float:left;"><h1>(?P<ime>.+?)</h1></div>.*?'
    r'<div class="g2"><b>Gorovje:</b> <a class="moder" href=".*?">(?P<gorovje>.+?)</a></div>.*?'
    r'<div class="g2"><b>Višina:</b> (?P<visina>.+?)&nbsp;m</div>.*?'
    r'<div class="g2"><b>Vrsta:</b> (?P<vrsta>.+?)</div>.*?'
    r'<div class="g2"><b>Ogledov:</b> (?P<ogledi>.+?)</div>.*?'
    r'<div class="g2"><b>Priljubljenost:</b> (?P<priljubljenost>.+?)%.*?</div>.*?'
    r'<div class="g2"><b>Število slik:</b> <a class="moder" href="#slike">(?P<st_slik>.+?)</a></div>.*?'
    r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(?P<st_poti>.+?)</a></div>.*?',
    flags=re.DOTALL
)
#Iz HTML-ja izločimo samo podatke, ki nas zanimajo.

def izloci_podatke(blok):
    gora = vzorec_gore.search(blok).groupdict() 
    gora['visina'] = int(gora['visina'])
    gora['ogledi'] = int(gora['ogledi'].replace(".", ""))
    gora['st_slik'] = int(gora['st_slik'])
    gora['st_poti'] = int(gora['st_poti'])
    return gora

def seznam_slovarjev(hribovje): #lahko narediš tudi za vsa hribovja
    i = 1
    seznam = []
    while os.path.isfile(f'podatki/{hribovje}/hrib {i}') == True:
        vsebina = file_content(f'podatki/{hribovje}/hrib {i}')
        for blok in vzorec_bloka.finditer(vsebina):
            seznam.append(izloci_podatke(blok.group(0))) 
        i += 1
    return seznam

def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return "A morem jaz kaj vračat?"

def gore_v_csv(seznam_gora, mapa, datoteka):
    assert seznam_gora and (all(slovar.keys() == seznam_gora[0].keys() for slovar in seznam_gora))
    imena_stolpcev = sorted(seznam_gora[0])
    write_csv(imena_stolpcev, seznam_gora, mapa, datoteka
)

# veliki_seznam = []
# for j in range(1, 11):
#     mali_seznam = seznam_slovarjev(f"hribovje {j}")
#     veliki_seznam.extend(mali_seznam)
# print (len(veliki_seznam))
