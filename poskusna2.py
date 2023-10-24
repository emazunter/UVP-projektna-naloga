import re
def loci_po_vejicah(niz):
    seznam = []
    for i in range(len(niz)):
        if niz[i] == ",":
            seznam.append(niz[:i])
            print(seznam)
            loci_po_vejicah(niz[(i+1):])
    return seznam

loci_po_vejicah("fefw, sdaf, fds")

vzorec_osebe = re.compile(
    r'<a\s+href="/name/nm(?P<id>\d+)/?[^>]*?>(?P<ime>.+?)</a>',
    flags=re.DOTALL)

def izloci_osebe(niz):
    osebe = []
    for oseba in vzorec_osebe.finditer(niz):
        osebe.append({
            'id': int(oseba.groupdict()['id']),
            'ime': oseba.groupdict()['ime'],
        })
    return osebe

def izloci_podatke_filma(blok):
    film['reziserji'] = izloci_osebe(film['reziserji'])
    # zabeležimo oznako, če je omenjena
