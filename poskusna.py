import preberi_podatke
import re
import os
vzorec_blok_gora = re.compile(
    r'<tr class="vr.*?&nbsp;m',
    re.DOTALL
)
vzorec_ime_in_url = re.compile(
    r'<tr class="vr.*?<a href="(?P<url>.*?)"'
    r'>(?P<ime>.+?)<.*?\1"',
    re.DOTALL
)
vzorec_podatki = re.compile(
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
vzorec_html_izhodisca = re.compile(
    r'<tr.*?</tr>',
    re.DOTALL
)
vzorec_izhodisca = re.compile(
    r'<a href="(?P<url>.*?)">(?P<izhodisce>.*?)\s-.*?'
    r'<a.*?>(?P<cas>.*?)<.*?<a.*?'
    r'>(?P<zahtevnost>.*?)<',
    re.DOTALL
)
vzorec_ime_poti = re.compile(r'<a.*?\s-.*?\((?P<pot>.*?)\)<', re.DOTALL)
vzorec_visina_izhodisca = re.compile(r'<b>Izhodišče:.*?\((?P<visinaizh>\d*?) ', re.DOTALL)
vzorec_koordinate = re.compile(r'Širina.*?span.*?>(?P<koordinate>.*?)<', re.DOTALL)


######################################################
def preveri_obstoj_datoteke(ime_datoteke):
    return os.path.isfile(ime_datoteke)

def najdi_vzorec_v_datoteki(ime_datoteke, vzorec):
    niz = vsebina_datoteke(ime_datoteke)
    seznam = []
    for pojavitev in re.finditer(vzorec, niz): #finditer vrne matchobject (kot string)
        ujemanje = pojavitev.groupdict() #groupdict naredi iz matchobjectov slovar z groupname as keys and matched strings valuse
        seznam.append(ujemanje)
    return seznam


# Iz vsake spletne strani za posamezen vrh moramo ven pobrati podatke o vrhu in jih zapisati v slovar. 
# Hkrati še iz bloka poti poberem podatke in jih shranimo v podslovar.
seznam_podatki_vrhov = []
for j in range(i):
    k = 0 
    while orodja.preveri_obstoj_datoteke(f'shranjene_strani/gorovje{j}/vrh{j}.{k}') == True:
        podatki = orodja.najdi_vzorec_v_datoteki(f'shranjene_strani/gorovje{j}/vrh{j}.{k}', orodja.vzorec_podatki_gore)
        for slovar_vrh in podatki:
            blok_poti = slovar_vrh.get('blok_poti')
            slovar_poti = orodja.najdi_vzorec_v_nizu(blok_poti, orodja.vzorec_podatki_pot)
            slovar_vrh['blok_poti'] = slovar_poti
            slovar_vrh = orodja.popravi_podatke_vrh(slovar_vrh)
        seznam_podatki_vrhov += podatki
        k += 1
        
        print(f'v seznam dodan vrh{j}.{k}')
        print(f'v seznamu je {len(seznam_podatki_vrhov)} vrhov.')
print(f'Seznam vrhov je končan, shranjenih je bilo {len(seznam_podatki_vrhov)} vrhov.')

# search = Scan through string looking for the first location where this regular expression produces a match, and return a corresponding Match. Return None if no position in the string matches the pattern; 
    #print(gora) # ne dela
MOJI:
vzorec_gore = re.compile(
    r'<div class="naslov1"><div style="float:left;"><h1>(?P<ime>.+?)</h1></div>.*?'
    r'<div class="g2"><b>Gorovje:</b> <a class="moder" href=".*?">(?P<gorovje>.+?)</a></div>.*?'
    r'<div class="g2"><b>Višina:</b> (?P<visina>.+?)&nbsp;m</div>.*?'
    r'<div class="g2"><b>Vrsta:</b> (?P<vrsta>.+?)</div>.*?'
    r'<div class="g2"><b>Ogledov:</b> (?P<ogledi>.+?)</div>.*?'
    r'<div class="g2"><b>Priljubljenost:</b> (?P<priljubljenost_procenti>\d+%)&nbsp;((?P<priljubljenost_mesto>\d+\.)&nbsp;mesto)</div>.*?'
    r'<div class="g2"><b>Število slik:</b> <a class="moder" href="#slike">(?P<st_slik>.+?)</a></div>.*?'
    r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(?P<st_poti>.+?)</a></div>.*?'
    r'<div style="padding-top:10px;"><b>Opis.*?:</b><br />(?P<opis>.+?)</div>.*?'
    r'<table class="TPoti" id="poti">(?P<poti>.+?)</table>',
    flags=re.DOTALL

    Novi:

    vzorec_gore = re.compile(
    r'<div class="naslov1"><div style="float:left;"><h1>(?P<ime>.+?)</h1></div>.*?'
    r'<div class="g2"><b>Gorovje:</b> <a class="moder" href=".*?">(?P<gorovje>.+?)</a></div>.*?'
    r'<div class="g2"><b>Višina:</b> (?P<visina>.+?)&nbsp;m</div>.*?'
    r'<div class="g2"><b>Vrsta:</b> (?P<vrsta>.+?)</div>.*?'
    r'<div class="g2"><b>Ogledov:</b> (?P<ogledi>.+?)</div>.*?'
    r'<div class="g2"><b>Priljubljenost:</b> (?P<priljubljenost>.+?)%.*?</div>.*?'
    r'<div class="g2"><b>Število slik:</b> <a class="moder" href="#slike">(?P<st_slik>.+?)</a></div>.*?'
    r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(?P<st_poti>.+?)</a></div>.*?'
    r'<div style="padding-top:10px;"><b>Opis.*?:</b><br />(?P<opis>.+?)</div>.*?'
    r'<table class="TPoti" id="poti">(?P<poti>.+?)</table>',
    flags=re.DOTALL
