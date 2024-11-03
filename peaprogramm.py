import json


def andmete_lisamine(failinimi, nimi, koordinaat, grupp, vooluvajadus, kommentaar, vajalikud_esemed):
    andme_fail = open(failinimi, 'w', encoding='utf-8')


    andme_fail.close()

def lisa_sonastikku(sonastik, punkti_nimi):
    sonastik[punkti_nimi] = {
        'nimi': '',
        'koordinaat': (),
        'grupp': '',
        'vooluvajadus': '',
        'kommentaar': '',
        'vajalikud_esemed': {}
    }

def muuda_nime(sonastik, punkti_nimi, nimi):
    sonastik[punkti_nimi]['nimi'] = nimi


def muuda_koodinaate(sonastik, punkti_nimi, koordinaat):
    sonastik[punkti_nimi]['koordinaat'] = koordinaat


def muuda_gruppi(sonastik, punkti_nimi, grupp):
    sonastik[punkti_nimi]['grupp'] = grupp


def muuda_vooluvajadust(sonastik, punkti_nimi, vooluvajadus):
    sonastik[punkti_nimi]['vooluvajadus'] = vooluvajadus


def muuda_kommentaari(sonastik, punkti_nimi, kommentaar):
    sonastik[punkti_nimi]['kommentaar'] = kommentaar


def muuda_vajalike_esemeid(sonastik, punkti_nimi, vajalikud_esemed):
    sonastik[punkti_nimi]['vajalikud_esemed'] = vajalikud_esemed


def lisa_vajalik_ese(sonastik, punkti_nimi, vajalik_ese, kogus = 1):
    if vajalik_ese in sonastik[punkti_nimi]['vajalikud_esemed']:
        sonastik[punkti_nimi]['vajalikud_esemed'][vajalik_ese] += kogus
    else:
        sonastik[punkti_nimi]['vajalikud_esemed'][vajalik_ese] = kogus


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



andme_sonastik = {
    'punkt1': {
             'nimi': 'Punkt1',
             'koordinaat': (1234, 720),
             'grupp': 'Esimene grupp',
             'vooluvajadus': 1200,
             'kommentaar': '',
             'vajalikud_esemed': {'10 meetrine 16A kaabel': 1, '5 meetrine 16A kaabel': 3, '16A alajaotusjaam': 1}
             },

    'punkt2': {'nimi': 'Punkt2',
             'koordinaat': (123, 360),
             'grupp': 'Esimene grupp',
             'vooluvajadus': 1500,
             'kommentaar': 'See on kommentaar',
             'vajalikud_esemed': {'10 meetrine 16A kaabel': 1}
             }
}

# print(andme_sonastik['punkt2']['grupp'])
# lisa_sonastikku(andme_sonastik, 'punkt3')
# muuda_nime(andme_sonastik, 'punkt3', 'Meie pannkoogid')
# lisa_vajalik_ese(andme_sonastik, 'punkt2', '15 meetrine 16A kaabel', 3)
#
# print(andme_sonastik)
#
# prindi_punkti_andmed(andme_sonastik, input('Sisesta punkti nimi'))

while True:
    sisend = input('Sisesta funktsioon: ')
    if sisend == 'break':
        break

    if sisend == 'andmed':
        prindi_punkti_andmed(andme_sonastik, input('Sisesta punkti nimi: '))

    if sisend == 'salvesta':
        fnimi = input('Sisesta failinimi: ')
        if fnimi:
            failinimi = fnimi
        salvesta_faili(andme_sonastik, failinimi)

    if sisend == 'lisa_sonastikku':
        punkti_nimi = input('Mis punkti soovid lisada: ')
        lisa_sonastikku(andme_sonastik, punkti_nimi)
    if sisend == 'muuda':
        punkti_nimi = input('Mis punkti soovid muuta: ')
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
