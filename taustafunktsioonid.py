import json


def lisa_sonastikku(sonastik, punkti_nimi):
    sonastik[punkti_nimi] = {
        'nimi': '',
        'koordinaat': (),
        'värv': '',
        'grupp': '',
        'vooluvajadus': 0,
        'seadmed': {},
        'kommentaar': '',
        'vajalikud esemed': {}
    }

def muuda_nime(sonastik, punkti_nimi, nimi):
    sonastik[punkti_nimi]['nimi'] = nimi


def muuda_koordinaate(sonastik, punkti_nimi, koordinaat):
    sonastik[punkti_nimi]['koordinaat'] = koordinaat


def muuda_varvi(sonastik, punkti_nimi, varv):
    sonastik[punkti_nimi]['värv'] = varv


def muuda_gruppi(sonastik, punkti_nimi, grupp):
    sonastik[punkti_nimi]['grupp'] = grupp
    if grupp:
        if grupp not in sonastik:
            sonastik[grupp] = {
                'grupi vooluvajadus': 0,
                'grupi vajalikud esemed': {}
            }
    uuenda_grupi_vooluvajadust(sonastik)
    uuenda_grupi_esemeid(sonastik)

def muuda_vooluvajadust(sonastik, punkti_nimi, vooluvajadus):
    sonastik[punkti_nimi]['vooluvajadus'] = vooluvajadus
    uuenda_grupi_vooluvajadust(sonastik)


def muuda_seadmeid(sonastik, punkti_nimi, seadmed):
    sonastik[punkti_nimi]['seadmed'] = seadmed


def muuda_kommentaari(sonastik, punkti_nimi, kommentaar):
    sonastik[punkti_nimi]['kommentaar'] = kommentaar


def muuda_vajalike_esemeid(sonastik, punkti_nimi, vajalikud_esemed):
    sonastik[punkti_nimi]['vajalikud esemed'] = vajalikud_esemed


def lisa_vajalik_ese(sonastik, punkti_nimi, vajalik_ese, kogus = 1):
    if vajalik_ese in sonastik[punkti_nimi]['vajalikud esemed']:
        sonastik[punkti_nimi]['vajalikud esemed'][vajalik_ese] += kogus
    else:
        sonastik[punkti_nimi]['vajalikud esemed'][vajalik_ese] = kogus
    uuenda_grupi_esemeid(sonastik)


def salvesta_faili(sonastik, failinimi):
    fail = open(failinimi, 'w', encoding='utf-8')
    json.dump(sonastik, fail, ensure_ascii=False, indent=4)
    fail.close
    print('Salvestati')

def impordi(failinimi):
    with open(failinimi, 'r', encoding='utf-8') as fail:
        global sonastik
        sonastik = json.load(fail)


def uuenda_grupi_vooluvajadust(sonastik):
    # nulli grupi vooluvajaduse
    for voti in sonastik:
        if isinstance(sonastik[voti], dict) and 'grupi vooluvajadus' in sonastik[voti]:
            sonastik[voti]['grupi vooluvajadus'] = 0

    #arvutab iga grupi vooluvajaduse
    for punkt, andmed in sonastik.items():
        if 'grupp' in andmed and andmed['grupp'] in sonastik:
            grupp = andmed['grupp']
            sonastik[grupp]['grupi vooluvajadus'] += int(andmed.get('vooluvajadus', 0))


def uuenda_grupi_esemeid(sonastik):
    # nulli grupi vooluvajaduse
    for voti in sonastik:
        if isinstance(sonastik[voti], dict) and 'grupi vajalikud esemed' in sonastik[voti]:
            sonastik[voti]['grupi vajalikud esemed'] = {}

    # arvutab iga grupi vooluvajaduse
    for punkt, andmed in sonastik.items():
        if 'grupp' in andmed and andmed['grupp'] in sonastik:
            grupp = andmed['grupp']
            for ese, kogus in andmed.get('vajalikud esemed', {}).items():
                if ese in sonastik[grupp]['grupi vajalikud esemed']:
                    sonastik[grupp]['grupi vajalikud esemed'][ese] += kogus
                else:
                    sonastik[grupp]['grupi vajalikud esemed'][ese] = kogus


def koik_andmed_teksti(sonastik, failinimi):
    print('Hello world')
    with open(failinimi, 'w', encoding='utf-8') as fail:
        for grupp, andmed in sonastik.items():
            if 'grupp' not in andmed:
                fail.write(f'Grupp: {grupp}\n')
                fail.write(f'Grupi vooluvajadus {andmed["grupi vooluvajadus"]}\n')
                fail.write(f'Gruppi kuuluvad punktid:\n')
                for punkt2, andmed2 in sonastik.items():
                    if andmed2['grupp'] == grupp:
                        fail.write(f'Nimi: {andmed2['nimi']}\n')
                        fail.write(f'Elektrikapp: {andmed2['kapp']}\n')
                        fail.write(f'Vooluvajadus kokku: {andmed2['vooluvajadus']}\n')
                        fail.write(f'Seadmed:\n')
                        for seade in andmed2['seadmed']:
                            fail.write(f'{seade}: {andmed2['seadmed'][seade]}W\n')
                        fail.write(f'Kommentaarid:\n')
                        fail.write(f'{andmed2['kommentaar']}\n\n')
