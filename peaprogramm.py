import json


def lisa_sonastikku(sonastik, punkti_nimi):
    sonastik[punkti_nimi] = {
        'nimi': '',
        'koordinaat': (),
        'grupp': '',
        'vooluvajadus': 0,
        'kommentaar': '',
        'vajalikud esemed': {}
    }

def muuda_nime(sonastik, punkti_nimi, nimi):
    sonastik[punkti_nimi]['nimi'] = nimi


def muuda_koodinaate(sonastik, punkti_nimi, koordinaat):
    sonastik[punkti_nimi]['koordinaat'] = koordinaat


def muuda_gruppi(sonastik, punkti_nimi, grupp):
    sonastik[punkti_nimi]['grupp'] = grupp
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


def prindi_punkti_andmed(sonastik, punkti_nimi):
    for kategooria in sonastik[punkti_nimi]:
        print(f'{kategooria}: {sonastik[punkti_nimi][kategooria]}')


def str_to_koordinaat(koordinaat):
    koordinaadid = [x.strip() for x in koordinaat.split(',')]
    return (int(koordinaadid[0]), int(koordinaadid[1]))


def salvesta_faili(sonastik, failinimi):
    fail = open(failinimi, 'w', encoding='utf-8')
    json.dump(sonastik, fail, ensure_ascii=False, indent=4)
    fail.close


def impordi(failinimi):
    with open(failinimi, 'r', encoding='utf-8') as fail:
        global andme_sonastik
        andme_sonastik = json.load(fail)


def mis_punkt(sonastik):
    while True:
        punkti_nimi = input('Sisesta punkti nimi: ')
        if punkti_nimi in sonastik:
            return punkti_nimi
        else:
            print('Seda punkti ei ole, sisestage teine punkt')


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


# def arvuta_vool:


andme_sonastik = {}


while True:
    sisend = input('Sisesta funktsioon: ')
    if sisend == 'break':
        break

    if sisend == 'andmed':
        prindi_punkti_andmed(andme_sonastik, mis_punkt(andme_sonastik))

    if sisend == 'salvesta':
        fnimi = input('Sisesta failinimi: ')
        if fnimi:
            failinimi = fnimi
        salvesta_faili(andme_sonastik, failinimi)

    if sisend == 'impordi':
        failinimi = input('Sisesta failinimi: ')
        improdi_kinnitus = input('Oled sa kindel, et soovid sonastiku yle kirjutada? ')
        if improdi_kinnitus == 'jah':
            impordi(failinimi)

    if sisend == 'lisa_sonastikku':
        lisa_sonastikku(andme_sonastik, input('Sisestage punkti nimi: '))
    if sisend == 'muuda':
        punkti_nimi = mis_punkt(andme_sonastik)
        while True:
            prindi_punkti_andmed(andme_sonastik, punkti_nimi)
            kategooria = input('Mis kategooriat soovid muuta: ')
            if kategooria == 'all':
                nimi = input('Sisesta nimi: ')
                if nimi:
                    muuda_nime(andme_sonastik, punkti_nimi, nimi)
                koordinaat = input('Sisesta koordinaadid: ')
                if koordinaat:
                    muuda_koodinaate(andme_sonastik, punkti_nimi, str_to_koordinaat(koordinaat))
                grupp = input('Sisesta grupi nimi: ')
                if grupp:
                    muuda_gruppi(andme_sonastik, punkti_nimi, grupp)
                vooluvajadus = input('Sisesta vooluvajadus: ')
                if vooluvajadus:
                    muuda_vooluvajadust(andme_sonastik, punkti_nimi, int(vooluvajadus))
                kommentaar = input('Sisesta kommentaar: ')
                if kommentaar:
                    muuda_kommentaari(andme_sonastik, punkti_nimi, kommentaar)
                vajalikud_esemed = input('Sisesta vajalikud esemed: ')
                if vajalikud_esemed:
                    while True:
                        ese = input('Sisesta vajalik ese: ')
                        if ese == '':
                            break
                        kogus = int(input('Sisesta kogus: '))
                        lisa_vajalik_ese(andme_sonastik, punkti_nimi, ese, kogus)
                break
            if kategooria == 'nime':
                nimi = input('Sisesta nimi: ')
                if nimi:
                    muuda_nime(andme_sonastik, punkti_nimi, nimi)
            if kategooria == 'koordinaate':
                koordinaat = input('Sisesta koordinaadid: ')
                if koordinaat:
                    muuda_koodinaate(andme_sonastik, punkti_nimi, str_to_koordinaat(koordinaat))
            if kategooria == 'gruppi':
                grupp = input('Sisesta grupi nimi: ')
                if grupp:
                    muuda_gruppi(andme_sonastik, punkti_nimi, grupp)
            if kategooria == 'vooluvajadust':
                vooluvajadus = input('Sisesta vooluvajadus: ')
                if vooluvajadus:
                    muuda_vooluvajadust(andme_sonastik, punkti_nimi, int(vooluvajadus))
            if kategooria == 'kommentaar':
                kommentaar = input('Sisesta kommentaar: ')
                if kommentaar:
                    muuda_kommentaari(andme_sonastik, punkti_nimi, kommentaar)
            if kategooria == 'vajalike esemeid':
                    while True:
                        ese = input('Sisesta vajalik ese: ')
                        if ese == 'break':
                            break
                        kogus = int(input('Sisesta kogus: '))
                        lisa_vajalik_ese(andme_sonastik, punkti_nimi, ese, kogus)

            if kategooria == 'break':
                break
            else:
                print('Sellist kategooriat pole')
