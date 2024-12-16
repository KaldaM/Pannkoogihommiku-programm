import json # Vajaliku andmete salvestamiseks ilusas formaadis

# Teeb sõnastikku vajalikud punktid
def lisa_sonastikku(sonastik, punkti_nimi):
    sonastik[punkti_nimi] = {
        'nimi': '',
        'koordinaat': (),
        'värv': '',
        'grupp': '',
        'vooluvajadus': 0,
        'seadmed': {},
        'kommentaar': '',
    }


def muuda_nime(sonastik, punkti_nimi, nimi):
    sonastik[punkti_nimi]['nimi'] = nimi


def muuda_varvi(sonastik, punkti_nimi, varv):
    sonastik[punkti_nimi]['värv'] = varv


def muuda_gruppi(sonastik, punkti_nimi, grupp):
    sonastik[punkti_nimi]['grupp'] = grupp
    if grupp:
        if grupp not in sonastik:
            sonastik[grupp] = {
                'grupi vooluvajadus': 0
            }
    uuenda_grupi_vooluvajadust(sonastik)


def muuda_vooluvajadust(sonastik, punkti_nimi, vooluvajadus):
    sonastik[punkti_nimi]['vooluvajadus'] = vooluvajadus
    uuenda_grupi_vooluvajadust(sonastik)


def muuda_seadmeid(sonastik, punkti_nimi, seadmed):
    sonastik[punkti_nimi]['seadmed'] = seadmed


def muuda_kommentaari(sonastik, punkti_nimi, kommentaar):
    sonastik[punkti_nimi]['kommentaar'] = kommentaar


 # Kirjutab ilusas ilusas formaadid sõnastiku faili
def salvesta_faili(sonastik, failinimi):
    fail = open(failinimi, 'w', encoding='utf-8')
    json.dump(sonastik, fail, ensure_ascii=False, indent=4)
    fail.close()
    print('Salvestati')


def uuenda_grupi_vooluvajadust(sonastik):
    # nullib grupi vooluvajaduse
    for voti in sonastik:
        if isinstance(sonastik[voti], dict) and 'grupi vooluvajadus' in sonastik[voti]:
            sonastik[voti]['grupi vooluvajadus'] = 0

    #arvutab iga grupi vooluvajaduse uuesti
    for punkt, andmed in sonastik.items():
        if 'grupp' in andmed and andmed['grupp'] in sonastik:
            grupp = andmed['grupp']
            sonastik[grupp]['grupi vooluvajadus'] += int(andmed.get('vooluvajadus', 0))


# Kirjutab sõnastikus olevad andmed kergesti loetavalt nii, et ei kuva ebavajalikku informatsiooni
def koik_andmed_teksti(sonastik, failinimi):
    with open(failinimi, 'w', encoding='utf-8') as fail:
        maaramata_grupp = False
        maaramata_vool = 0
        for punkt2, andmed2 in sonastik.items():
            if 'grupp' in andmed2 and andmed2['grupp'] == '':
                maaramata_grupp = True
                maaramata_vool += andmed2['vooluvajadus']


        for grupp, andmed in sonastik.items():
            if 'grupp' not in andmed:
                fail.write(f'Grupp: {grupp}\n')
                fail.write(f'Grupi vooluvajadus: {andmed["grupi vooluvajadus"]}\n')
                fail.write(f'Gruppi kuuluvad punktid:\n\n')
                for punkt2, andmed2 in sonastik.items():
                    if 'grupp' in andmed2 and andmed2['grupp'] == grupp:
                        if andmed2['nimi'] != '':
                            fail.write(f'Nimi: {andmed2['nimi']}\n')
                        else:
                            fail.write(f'Nimi: {punkt2}\n')
                        if andmed2['kapp'] != '':
                            fail.write(f'Elektrikapp: {andmed2['kapp']}\n')
                        fail.write(f'Vooluvajadus kokku: {andmed2['vooluvajadus']}\n')
                        if andmed2['seadmed'] != {}:
                            fail.write(f'Seadmed:\n')
                            for seade in andmed2['seadmed']:
                                fail.write(f'   {seade}: {andmed2['seadmed'][seade]}W\n')
                        if andmed2['kommentaar'] != '':
                            fail.write(f'Kommentaarid:\n')
                            read = andmed2['kommentaar'].split('\n')
                            for rida in read:
                                fail.write(f'   {rida.strip()}\n')
                            fail.write('\n')
                        else:
                            fail.write('\n')

                fail.write('--------------------------------------------\n\n')

        if maaramata_grupp:
            fail.write(f'Grupp: Määramata\n')
            fail.write(f'Grupi vooluvajadus: {maaramata_vool}\n')
            fail.write(f'Gruppi kuuluvad punktid:\n\n')
            for punkt2, andmed2 in sonastik.items():
                if 'grupp' in andmed2 and andmed2['grupp'] == '':
                    if andmed2['nimi'] != '':
                        fail.write(f'Nimi: {andmed2['nimi']}\n')
                    else:
                        fail.write(f'Nimi: {punkt2}\n')
                    if 'kapp' in andmed2 and andmed2['kapp'] != '':
                        fail.write(f'Elektrikapp: {andmed2['kapp']}\n')
                    fail.write(f'Vooluvajadus kokku: {andmed2['vooluvajadus']}\n')
                    if andmed2['seadmed'] != {}:
                        fail.write(f'Seadmed:\n')
                        for seade in andmed2['seadmed']:
                            fail.write(f'   {seade}: {andmed2['seadmed'][seade]}W\n')
                    if andmed2['kommentaar'] != '':
                        fail.write(f'Kommentaarid:\n')
                        read = andmed2['kommentaar'].split('\n')
                        for rida in read:
                            fail.write(f'   {rida.strip()}\n')
                        fail.write('\n')
                    else:
                        fail.write('\n')