################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Pannkoogihommiku programm alpha versioon
#
#
# Autorid: Matteus Kalda ja Ott Allik
#
# Lisakommentaar (nt käivitusjuhend): Programmis saab hetkel lisada vasaku nupuvajutusega faili, eemaldada, paremanupuvajutusega. Kui lisada punkt,
# on võimalik sisestada infot selle kohta, aga ei pea. Tuleb vajutada salvesta nuppu. Sõnastiku on võimalik importida ja exportida fail menüü kaudu.
# Selleks tuleb kasutada .txt failitüüpi.
# Külje peal on näha sõnastiku, et näha kuidas sisestatud andmed muutuvad. Tulevikus tuleks see parema välimusega ning interaktiivsem
# Kui punktid kuuluvad samasse gruppi, siis on sõnastikus näha punktide voolu summat.
##################################################

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.colorchooser import askcolor
from tkinter import ttk
from PIL import ImageTk, Image
import taustafunktsioonid
import json
import math


sonastik = {}


class ProgrammiGUI:
    def __init__(self):
        self.punkti_loendur = 1
        self.mõõdulindi_punktid = []
        self.mõõdulindi_jooned = []
        self.mõõdulindi_distantsid = []
        self.mõõdulindi_summa = 0
        self.summa_tekst = 0
        self.mõõdulindi_punktiloendur = 0
        self.suurus = 19.60 # suurus, mille järgi punktid moodustatakse. Hetkel tulevad punktid 3x3 meetrit
        self.root = tk.Tk()
        self.root.state('zoomed') # alustab progammi täissuuruses
        self.root.title("Koordinaatide valimine")


        # menu lisamine
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=exit)
        self.filemenu.add_command(label='Impordi', command=self.impordi_sonastik)
        self.filemenu.add_command(label='Salvesta', command=self.expordi_sonastik)
        self.filemenu.add_command(label='Kirjuta andmed tekstina', command=self.kirjuta_tekst)

        self.kujundus = tk.Menu(self.menubar, tearoff=0)
        self.kujundus.add_command(label='Vaheta ortofotole', command=self.vaheta_ortofoto)
        self.kujundus.add_command(label='Vaheta tavakaardile', command=self.vaheta_tavakaart)

        self.menubar.add_cascade(menu=self.filemenu, label='File')
        self.menubar.add_cascade(menu=self.kujundus, label='Kujundus')

        self.menubar.add_command(label='Kasutamise juhend', command=self.kasutamise_juhend)

        self.root.config(menu=self.menubar)

        # juhised kaardi kasutamiseks
        self.kaardijuhis = tk.StringVar()
        self.kaardijuhis.set(
            "Üleval menüüreal on võimalik avada detailne juhend programmi kasutamiseks"
        )
        self.silt = tk.Label(self.root, textvariable=self.kaardijuhis, font=("Arial", 12, "bold"))
        self.silt.pack(padx=15, pady=12, anchor="nw")

        # canvase tegemine
        self.canvas = tk.Canvas(self.root, width=1296, height=697)
        self.canvas.pack()
        self.canvas.place(relx=0.01, rely=0.05, anchor="nw")

        # canvasele kaardipildi panemine
        self.kaardipilt = ImageTk.PhotoImage(Image.open("tavakaart.png"))
        self.ortofoto = ImageTk.PhotoImage(Image.open('ortofoto.png'))
        self.canvas.create_image(648, 348.5, image=self.kaardipilt, tags='kaart')

        # Treeview info kuvamiseks
        self.tree = ttk.Treeview(self.root)
        self.tree.place(relx=1.0, rely=0, anchor='ne', relheight=1.0, width=400)
        self.tree.heading("#0", text="Sõnastik", anchor="w")
        self.uuenda_sonastiku_puu()

        # Aktiivne punktide liigutamine/lisamine
        self.mõõdulint_aktiivne = False
        self.mõõdulindi_reset_aktiivne = False
        self.liigutamine_aktiivne = False
        self.lisamine_aktiivne = False
        self.eemaldamine_aktiivne = True
        self.valitud_punkt = None

        # Nupud punktide lisamise ja liigutamise aktiveerimiseks ning mõõdulindi funktsiooni käivitamiseks
        self.mõõdulint_nupp = tk.Button(self.root, text="Mõõdulint", command=self.aktiveeri_mõõdulint)
        self.mõõdulint_nupp.place(relx=0.53, rely=0.78, anchor="center")

        self.lisa_nupp = tk.Button(self.root, text="Lisa punkte", command=self.aktiveeri_lisamine)
        self.lisa_nupp.place(relx=0.65, rely=0.78, anchor="center")

        self.liiguta_nupp = tk.Button(self.root, text="Liiguta punkte", command=self.aktiveeri_liigutamine)
        self.liiguta_nupp.place(relx=0.59, rely=0.78, anchor="center")


        # Canvase sündmuste sidumine
        self.canvas.bind("<Button-1>", self.canvas_vasakklikk)
        self.canvas.bind("<B1-Motion>", self.lohista_punkt)
        self.canvas.bind("<ButtonRelease-1>", self.lohistamise_lopp)
        self.canvas.bind("<Button-3>", self.canvas_paremklikk)
        self.canvas.bind("<Button-2>", self.muuda_ruudu_varvi)

        self.tree.bind("<<TreeviewSelect>>", self.treeview_item_selected)

        # Lisab canvasele programmi käivitamisel kappide asukohad, mis ei ole eemaldatavad ega liigutatavad
        self.lisa_kapid()
        self.valitud_canvas_id = None

        self.root.mainloop()


    # Annab detailse juhendi programmi funktsioonide kohta
    def kasutamise_juhend(self):
        juhend = """
    Üleval menüüreal on alamenüü "File". Selle kaudu on võimalik programm sulgeda (võib ka ristist sulgeda). 
    Teine funktsioon seal on import. Selle kaudu saad valida .txt faili, kuhu olid exportinud programmi sõnastiku. 
    See kustutab hetkel programmis olevad punktid ning asendab need failis olevate punktidega.
    Kolmas funktsioon seal on export. Sellega saad valida .txt faili, kuhu andmed salvestada. See salvestab kõik andmed. 
    Neljas funktsioon on "Kirjuta andmed tekstina", millega saad valida .txt faili, kuhu programm kirjutab sõnastikus olev info loetavalt ja jätab välja ebavajaliku info.

    Teine alamenüü on "Kujundus". Sealt saad vahetada ortofoto ja tavakaardi vahel.

    Programmis on paremal kujutatud kõik punktid ja grupid ning kapid. Kappidel on näha, palju nendes voolu alles on. 
    Gruppe on võimalik vahetada, muutes punktil grupi nime. Tabelis on võimalik punktidele vajutada ning see markeerib kaardil antud punkti ning avab punkti muutmise menüü.

    Kaardi all on kolm nuppu:
    1. Mõõdulint: vasaku klõpsuga mõõdad klikkide vahelisi vahemaid ning all paremal on vahemaade summa. Parema klikiga saab mõõdulindi jooned kustutada.
    2. Punktide liigutamine: hoia vasakut hiirenuppu punkti peal ja lohista.
    3. Punktide lisamine: vasaku klõpsuga lisad punkti, mis tuleb algselt punasena.

    Rullikul vajutamisega saad muuta punktide värvi. Kui mõõdulint pole aktiveeritud, saad parema klõpsuga punktil vajutades selle kustutada.

    Kui ükski nupp pole aktiveeritud, siis kaardil punktile vajutades avaneb andmete muutmise aken. 
    Seal saad määrata:
    - punkti nime,
    - grupi nime,
    - elektrikapi, millest punkt voolu võtab.

    Andmete muutmise aknas saad seadmeid lisada, muuta või kustutada. 
    Samuti saad lisada kommentaare punkti kohta.

    Kui vajutad kaardil kapile, siis näed, millised punktid sellele kapile määratud on ja palju need voolu vajavad.
    
    Küsimuste püsimise korral või programmi kõrvaltoimete tekkimisel pidage nõu arsti või Matteus Kaldaga.
    """
        # Kuvab juhendi dialoogiboksis
        juhendi_aken = tk.Toplevel(self.root)
        juhendi_aken.title("Programmi kasutamise juhend")
        juhendi_aken.geometry("850x700")

        # Lisame teksti keritavasse alasse
        scroll = tk.Scrollbar(juhendi_aken)
        text = tk.Text(juhendi_aken, wrap="word", font=("Arial", 12), yscrollcommand=scroll.set, bg="white")
        text.insert("1.0", juhend)
        text.config(state="disabled")  # Muuda tekst ainult loetavaks

        # Paigutus
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        scroll.config(command=text.yview)


    def lisa_kapid(self):
        """Lisab kaardile 7 elektrikappi, millest 2 on punased (32A) ja ülejäänud sinised."""
        kapid = [
            {"nimi": "PVK 1", "koordinaat": (459, 589), "vool": 11000, "värv": "#0000FF"},
            {"nimi": "PVK 2", "koordinaat": (679, 480), "vool": 22000, "värv": "#FF0000"},
            {"nimi": "PVK 3", "koordinaat": (908, 383), "vool": 11000, "värv": "#0000FF"},
            {"nimi": "PVK 10", "koordinaat": (255, 543), "vool": 11000, "värv": "#0000FF"},
            {"nimi": "PVK 9", "koordinaat": (348,315), "vool": 11000, "värv": "#0000FF"},
            {"nimi": "PVK 7", "koordinaat": (573, 262), "vool": 22000, "värv": "#FF0000"},
            {"nimi": "PVK 6", "koordinaat": (766, 210), "vool": 11000, "värv": "#0000FF"},
        ]
        # lisab kapile numbri alustades ühest
        for idx, kapp in enumerate(kapid, start=1):
            punkti_nimi = f'kapp{idx}'
            sonastik[punkti_nimi] = {
                "nimi": kapp["nimi"],
                "koordinaat": kapp["koordinaat"],
                "vooluvajadus": kapp["vool"],
                "värv": kapp["värv"],
                "grupp": "Kapid",
            }

            # Joonistab ringid kaardile
            ringi_suurus = 14

            item_id = self.canvas.create_oval(
                kapp["koordinaat"][0] - ringi_suurus / 2,
                kapp["koordinaat"][1] - ringi_suurus / 2,
                kapp["koordinaat"][0] + ringi_suurus / 2,
                kapp["koordinaat"][1] + ringi_suurus / 2,
                fill=kapp["värv"], outline="black", tags= "kapp"
            )
            sonastik[punkti_nimi]["canvas_id"] = item_id

        self.uuenda_sonastiku_puu()


    # TreeView ei uuenda oma andmeid automaatselt sõnastiku kaudu, nii et seda tuleb teha funktsiooni abil
    def uuenda_sonastiku_puu(self):
        self.tree.delete(*self.tree.get_children())  # Tühjenda TreeView

        grupi_node_id = {}  # Hoiab gruppide TreeView ID-d
        maaramata_vool = 0  # "Määramata" grupi koguvool

        # Esiteks loome grupid ja summeerime vooluvajadused
        for punkt_id, andmed in sonastik.items():
            if "koordinaat" in andmed:  # Ainult punktid, mitte grupiobjektid
                grupp = andmed.get("grupp", "Määramata")  # Kasuta vaikeväärtust "Määramata"

                if grupp == "Määramata":
                    # Summeerime määramata punktide voolu
                    maaramata_vool += andmed.get("vooluvajadus", 0)
                else:
                    # Kui gruppi pole veel lisatud, loome selle
                    if grupp not in grupi_node_id:
                        grupi_vool = sum(
                            punkt.get("vooluvajadus", 0)
                            for punkt in sonastik.values()
                            if punkt.get("grupp") == grupp
                        )
                        grupi_tekst = f"{grupp} - Vool: {grupi_vool}W"
                        grupi_node_id[grupp] = self.tree.insert("", "end", text=grupi_tekst, open=True)

                    # Lisa punkt gruppi
                    nimi = andmed.get("nimi", punkt_id)
                    vool = andmed.get("vooluvajadus", 0)
                    punkt_tekst = f"{nimi} - Vool: {vool}W"
                    värv = andmed.get("värv", "#FFFFFF")
                    self.tree.tag_configure(punkt_id, background=värv) # Lisab TreeViews punktile selle värvi, mis sellel ka kaardil on
                    self.tree.insert(grupi_node_id[grupp], "end", text=punkt_tekst, iid=punkt_id, tags=(punkt_id,))

        # Nüüd lisame määramata grupi
        if maaramata_vool > 0:  # Lisa ainult, kui voolu summa pole null
            maaramata_node = self.tree.insert("", "end", text=f"Määramata - Vool: {maaramata_vool}W", open=True)

            # Lisa määramata punktid selle grupi alla
            for punkt_id, andmed in sonastik.items():
                if "koordinaat" in andmed and andmed.get("grupp", "Määramata") == "Määramata":
                    nimi = andmed.get("nimi", punkt_id)
                    vool = andmed.get("vooluvajadus", 0)
                    punkt_tekst = f"{nimi} - Vool: {vool}W"
                    värv = andmed.get("värv", "#FFFFFF")
                    self.tree.tag_configure(punkt_id, background=värv)
                    self.tree.insert(maaramata_node, "end", text=punkt_tekst, iid=punkt_id, tags=(punkt_id,))


    # Highlightib kaardil punkti, mis TreeView kaudu valiti
    def treeview_item_selected(self, event):
        self.canvas.delete("highlight")  # Eemalda ainult highlight kastid

        selected_item = self.tree.selection()[0]  # TreeView elemendi ID vastab punkt-ID-le
        punkt_id = selected_item  # TreeView iids vastab punkt-ID-le

        if punkt_id in sonastik:
            punkt_data = sonastik[punkt_id]
            koordinaadid = punkt_data.get("koordinaat")

            if koordinaadid:
                # Highlight ainult valitud punkt
                self.highlight_punkt(koordinaadid[0], koordinaadid[1])
                # Ava andmete muutmise dialoog
                if punkt_id.startswith('kapp'):
                    self.naita_kapi_punkte(punkt_id)
                else:
                    self.andme_dialog(punkt_id)


    #Vasaku hiireklõpsu funktsioonid:
    def aktiveeri_mõõdulint(self):
        self.mõõdulint_aktiivne = not self.mõõdulint_aktiivne
        self.mõõdulindi_reset_aktiivne = not self.mõõdulindi_reset_aktiivne
        self.liigutamine_aktiivne = False  # Deaktiveerime liigutamise
        self.lisamine_aktiivne = False  # Deaktiveerime lisamise
        self.eemaldamine_aktiivne = not self.eemaldamine_aktiivne  # Deaktiveerime eemaldamise
        self.lisa_nupp.config(text="Lisa punkte")
        self.liiguta_nupp.config(text="Liiguta punkte")
        if self.mõõdulint_aktiivne:
            self.mõõdulint_nupp.config(text="Mõõdulint: Aktiivne")
        else:
            self.mõõdulint_nupp.config(text="Mõõdulint")
        self.valitud_punkt = None  # Eemaldame aktiivse valiku

    # aktiveerib lisamise võimaluse ning muudab nuppude tekste
    def aktiveeri_lisamine(self):
        self.lisamine_aktiivne = not self.lisamine_aktiivne
        self.eemaldamine_aktiivne = True
        self.mõõdulint_aktiivne = False  # Deaktiveerime mõõdulindi
        self.mõõdulindi_reset_aktiivne = False  # Deaktiveerime mõõdulindi reseti
        self.liigutamine_aktiivne = False  # Deaktiveerime liigutamise
        self.mõõdulint_nupp.config(text="Mõõdulint")
        self.liiguta_nupp.config(text="Liiguta punkte")
        if self.lisamine_aktiivne:
            self.lisa_nupp.config(text="Lisamine: Aktiivne")
        else:
            self.lisa_nupp.config(text="Lisa punkte")


    def aktiveeri_liigutamine(self):
        self.liigutamine_aktiivne = not self.liigutamine_aktiivne
        self.mõõdulint_aktiivne = False  # Deaktiveerime mõõdulindi
        self.mõõdulindi_reset_aktiivne = False  # Deaktiveerime mõõdulindi reseti
        self.lisamine_aktiivne = False  # Deaktiveerime lisamise
        self.eemaldamine_aktiivne = True  # Deaktiveerime eemaldamise
        self.mõõdulint_nupp.config(text="Mõõdulint")
        self.lisa_nupp.config(text="Lisa punkte")
        if self.liigutamine_aktiivne:
            self.liiguta_nupp.config(text="Liigutamine: Aktiivne")
        else:
            self.liiguta_nupp.config(text="Liiguta punkte")
        self.valitud_punkt = None  # Eemaldame aktiivse valiku


    # Parema hiireklõpsu funktsioonid eraldi (kui neid tuleb, praegu on kõik paralleelselt vasaku hiireklõpsu funktsioonidega):
    # ...
    def canvas_vasakklikk(self, event):
        if self.lisamine_aktiivne:
            self.lisa_ruut(event)  # Kui lisamine on aktiivne, lisa punkt
        elif self.liigutamine_aktiivne:
            self.vali_punkt(event)  # Kui liigutamine on aktiivne, vali punkt
        elif self.mõõdulint_aktiivne:
            self.mõõdulint(event)  # Kui mõõdulint on aktiivne, vali mõõdulindi funktsioon
        else:
            self.highlight_ja_muuda(event)  # Kui ükski pole aktiivne, highlight ja ava andmete muutmine


    def canvas_paremklikk(self, event):
        if self.mõõdulindi_reset_aktiivne:
            self.mõõdulindi_reset()
        elif self.eemaldamine_aktiivne:
            self.eemalda_ruut(event)


    def vali_punkt(self, event):
        if not self.liigutamine_aktiivne:
            return # teeb nii, et ei hakkaks punkti liigutama, kui me seda ei taha

        # Leia lähim lõuendi element
        valitud_id = self.canvas.find_closest(event.x, event.y)
        item_id = valitud_id[0]

        # Leia vastav punkt sõnastikust
        for punkt_id, andmed in sonastik.items():
            if "canvas_id" in andmed and andmed["canvas_id"] == item_id:
                self.valitud_punkt = punkt_id
                self.valitud_canvas_id = item_id
                break


    def lohista_punkt(self, event):
        if not self.liigutamine_aktiivne or not self.valitud_punkt:
            return # kontrollib, kas soovime lohistada

        if 'kapp' in self.canvas.gettags(self.valitud_canvas_id):
            return # eemaldab kappide liigutamise võimaluse

        x, y = event.x, event.y

        # Uuenda lõuendi elemendi koordinaate
        self.canvas.coords(
            self.valitud_canvas_id,
            x - self.suurus / 2, y - self.suurus / 2,
            x + self.suurus / 2, y + self.suurus / 2
        )

        # Tõsta lõuendi element teiste kohale (valikuline)
        self.canvas.tag_raise(self.valitud_canvas_id)

        # Uuenda sõnastikus punkti koordinaate
        sonastik[self.valitud_punkt]['koordinaat'] = (x, y)


    def lohistamise_lopp(self, event):
        if not self.liigutamine_aktiivne or not self.valitud_punkt or not self.mõõdulint_aktiivne:
            return

        # Uuenda sõnastikus punkti koordinaate
        x, y = event.x, event.y
        sonastik[self.valitud_punkt]['koordinaat'] = (x, y)
        self.valitud_punkt = None
        self.valitud_canvas_id = None
        self.uuenda_punktid()  # Värskenda kõiki punkte kaardil


    def mõõdulint(self, event):
        x, y = event.x, event.y
        värv = "#000000"  # Vaikimisi must värv

        # Loome mõõdulindi otspunkti
        mõõdulindi_punkt = self.canvas.create_oval(
            x - 3, y - 3,
            x + 3, y + 3,
            fill=värv
        )

        # Muutujat mõõdulindi_punkt kasutatakse mõõdulindi resettimisel ja muutujaid x ja y järgnevate joonte ja omavahelise distantsi arvutamiseks
        self.mõõdulindi_punktid.append([mõõdulindi_punkt, [x, y]])

        # Loome joone(d) otspunktide vahele
        if len(self.mõõdulindi_punktid) >= 2:
            mõõdulindi_joon = (
                                self.canvas.create_line(self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1][0], self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1][1],
                               self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1][0], self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1][1],
                               fill=värv, width=2)
            )

            self.mõõdulindi_jooned.append(mõõdulindi_joon) #Lisame jooned listi, et neid saaks hiljem resettida

            # Loome vahemaa punktide vahele, teisendame meetriteks
            vahemaa = round(math.dist(self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1],
                               self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1]) / 6.4635, 2
            )
            self.mõõdulindi_summa += vahemaa

            # Kuvame canvasele kahe punkti vahelise distantsi
            vahemaa_tekst = self.canvas.create_text((self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1][0] + self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1][0]) / 2,
                               ((self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1][1] + self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1][1]) / 2) + 15,
                               text=f'{vahemaa} m', fill="black", font=("bold", 10))

            self.canvas.delete(self.summa_tekst)
            self.summa_tekst = self.canvas.create_text(1000, 650, text=f'Vahemaa kokku: {round(self.mõõdulindi_summa,2)}', fill='black', font=('bold', 15))

            self.mõõdulindi_distantsid.append(vahemaa_tekst)  # Lisame vahemaad listi, et neid saaks hiljem resettida

            self.mõõdulindi_punktiloendur += 1


    def mõõdulindi_reset(self):
        # Kustutame canvaselt kõik mõõdulindiga seotud elemendid
        for element in self.mõõdulindi_punktid:
            self.canvas.delete(element[0])
        for element in self.mõõdulindi_jooned:
            self.canvas.delete(element)
        for element in self.mõõdulindi_distantsid:
            self.canvas.delete(element)
        self.canvas.delete(self.summa_tekst)

        # Tühjendame mõõdulindiga seotud listid, et neid saaks uue mõõdulindi loomisel kasutada
        self.mõõdulindi_punktid.clear()
        self.mõõdulindi_jooned.clear()
        self.mõõdulindi_distantsid.clear()

        # Nullime punktiloenduri ja summa
        self.mõõdulindi_punktiloendur = 0
        self.mõõdulindi_summa = 0


    def highlight_ja_muuda(self, event):
        # Leia lähim punkt
        for punkt_id, andmed in sonastik.items():
            if "koordinaat" in andmed:
                x, y = andmed["koordinaat"]
                if abs(x - event.x) < 10 and abs(y - event.y) < 10:  # Kui klõps on punkti lähedal
                    if punkt_id.startswith('kapp'):
                        self.naita_kapi_punkte(punkt_id)
                        return # Teeb nii, et kapil vajutamine ei avaks andme dialogi
                    else:
                        self.highlight_punkt(x, y)  # Highlight punkt
                        self.andme_dialog(punkt_id)  # Ava andmete dialoog
                        break


    # Võimaldab kasutajal valida .txt fail, millele on kirjutatud sõnastik, mida importida
    def impordi_sonastik(self):
        failitee = filedialog.askopenfilename(title='Vali fail', filetypes=[('txt failid', '*.txt'), ('All Files', '.*')])

        if failitee:
            with open(failitee, 'r', encoding='utf-8') as fail:
                andmed = json.load(fail)
                global sonastik
                sonastik.clear()
                sonastik.update(andmed)
                print('Andmed imporditud', sonastik)
                self.uuenda_punktid()


        # Leia suurim olemasolev punktinumber ja uuenda punkti_loendur
        punktinumbrid = [
            int(key.split('-')[1]) for key in sonastik.keys() if key.startswith("punkt-") and key.split('-')[1].isdigit()
        ]
        if punktinumbrid:
            self.punkti_loendur = max(punktinumbrid) + 1
        else:
            self.punkti_loendur = 1  # Alusta uuesti ühest, kui punkte ei leidu

        self.uuenda_sonastiku_puu()


    # Teeb lilla ruudu ümber punkti ning kustutab enne eelmise highlighti ära
    def highlight_punkt(self, x, y):
        self.canvas.delete("highlight")
        self.canvas.create_rectangle(
            x - self.suurus / 2, y - self.suurus / 2, x + self.suurus / 2, y + self.suurus / 2,
            outline="purple", width=3, tags="highlight"
        )


    # Taustafunktsiooni abil dumpib json abil sõnastiku kasutaja valitud .txt faili
    def expordi_sonastik(self):
        salvestuskoht = filedialog.askopenfilename(title='Vali fail', filetypes=[('txt failid', '*.txt'), ('All Files', '.*')])

        if salvestuskoht:
            global sonastik
            taustafunktsioonid.salvesta_faili(sonastik, salvestuskoht)


    def kirjuta_tekst(self):
        salvestuskoht = filedialog.askopenfilename(title='Vali fail', filetypes=[('txt failid', '*.txt'), ('All Files', '.*')])

        if salvestuskoht:
            global sonastik
            taustafunktsioonid.koik_andmed_teksti(sonastik, salvestuskoht)


    # Vahetab kaardi satelliitpildile
    def vaheta_ortofoto(self):
        self.canvas.delete('kaart')
        self.canvas.create_image(648, 348.5, image=self.ortofoto, tags='kaart')
        self.canvas.tag_lower('kaart')  # Aseta kaardikiht lõuendi kõige alla


    # Vahetab kaardi elektriskeemidega puhtale kaardile
    def vaheta_tavakaart(self):
        self.canvas.delete('kaart')
        self.canvas.create_image(648, 348.5, image=self.kaardipilt, tags='kaart')
        self.canvas.tag_lower('kaart')  # Aseta kaardikiht lõuendi kõige alla


    # Kuna Tkinter automaatselt punkte ei uuenda, tuleb seda teha funktsiooni abil
    def uuenda_punktid(self):
        # Eemalda kõik punktid lõuendilt
        self.canvas.delete('punkt')

        # Joonista kõik punktid uuesti sõnastikust
        for punkt_id, andmed in sonastik.items():
            if "koordinaat" in andmed and not punkt_id.startswith('kapp'):
                x, y = andmed["koordinaat"]
                värv = andmed.get("värv", "#FF0000")  # Vaikimisi punane värv

                # Joonista punkt lõuendile ja salvesta lõuendi elemendi ID
                item_id = self.canvas.create_rectangle(
                    x - self.suurus / 2, y - self.suurus / 2,
                    x + self.suurus / 2, y + self.suurus / 2,
                    fill=värv, outline="black", tags=(punkt_id, "punkt")
                )
                andmed['canvas_id'] = item_id  # Salvesta lõuendi elemendi ID


    # Võimaldab 3x3 meetriseid ruute lisada kaardile. Need peaksid kujutama telke.
    def lisa_ruut(self, event):
        x, y = event.x, event.y
        värv = "#FF0000"  # Vaikimisi punane värv
        punkti_nimi = f'punkt-{self.punkti_loendur}'

        # Lisa punkt sõnastikku
        taustafunktsioonid.lisa_sonastikku(sonastik, punkti_nimi) # Loob sõnastikus õiged kategooriad
        sonastik[punkti_nimi]['koordinaat'] = (x, y)
        sonastik[punkti_nimi]['värv'] = värv

        # Tee punkt kohe nähtavaks ja salvesta lõuendi elemendi ID
        item_id = self.canvas.create_rectangle(
            x - self.suurus / 2, y - self.suurus / 2,
            x + self.suurus / 2, y + self.suurus / 2,
            fill=värv, outline="black", tags=(punkti_nimi, "punkt")
        )
        sonastik[punkti_nimi]['canvas_id'] = item_id  # Salvesta lõuendi elemendi ID

        self.punkti_loendur += 1
        self.uuenda_sonastiku_puu()  # Värskenda TreeView

    # Eemaldab kaardilt punkti
    def eemalda_ruut(self, event):
        if not self.eemaldamine_aktiivne:
            return

        kustutatav = self.canvas.find_closest(event.x, event.y)[0]
        vajutatud_punkt = self.canvas.coords(kustutatav)
        punktikese_x = (vajutatud_punkt[0] + vajutatud_punkt[2]) / 2
        punktikese_y = (vajutatud_punkt[1] + vajutatud_punkt[3]) / 2
        punktikese_koordinaadid = (int(punktikese_x), int(punktikese_y))


        for punkt in list(sonastik.keys()):
            if punkt.startswith('punkt') and punktikese_koordinaadid == tuple(sonastik[punkt]["koordinaat"]):
                punkti_nimi = sonastik[punkt]['nimi']
                if punkti_nimi == '':
                    punkti_nimi = punkt # Teeb nii, et kui punktile pole nime määratud, on punki nimeks selle sõnastiku võti
                if messagebox.askyesno(title='Kustuta?', message=f"Kas oled kindel, et soovid {punkti_nimi} eemaldada?"): # Küsib kasutajalt üle, kas ta soovib ikka punkti kustutada
                    # Kapile voolu taastamine
                    seotud_kapp = sonastik[punkt].get('kapp', '')
                    if seotud_kapp:
                        for kapp_id, kapp_andmed in sonastik.items():
                            if kapp_andmed.get('nimi') == seotud_kapp:
                                kapp_andmed['vooluvajadus'] += sonastik[punkt]['vooluvajadus'] # Tagastab voolu, mis punkti kapilt nõudis

                    # Eemalda ruut lõuendilt ja sõnastikust
                    self.canvas.delete(kustutatav)
                    self.canvas.delete("highlight")
                    grupp = sonastik[punkt]['grupp']
                    del sonastik[punkt]

                    # Kontrolli, kas grupp on tühi, ja eemalda see
                    if grupp and grupp in sonastik:
                        grupi_punktid = [p for p in sonastik if sonastik[p].get('grupp') == grupp]
                        if not grupi_punktid:  # Kui grupis pole enam punkte
                            del sonastik[grupp]
                            print(f"Grupp {grupp} on kustutatud, sest see on tühi.")
                    break

        self.uuenda_sonastiku_puu()


    def muuda_ruudu_varvi(self, event):
        # Leia ruut, millel klikiti
        valitud_ruut = self.canvas.find_closest(event.x, event.y)[0]
        ruudu_koordinaadid = self.canvas.coords(valitud_ruut)
        punktikese_x = (ruudu_koordinaadid[0] + ruudu_koordinaadid[2]) / 2
        punktikese_y = (ruudu_koordinaadid[1] + ruudu_koordinaadid[3]) / 2
        punktikese_koordinaadid = (int(punktikese_x), int(punktikese_y))

        # Leia vastav punkt sõnastikust
        for el in sonastik:
            if el.startswith('punkt') and punktikese_koordinaadid == tuple(sonastik[el]["koordinaat"]):
                # Küsi uus värv
                uus_varv = askcolor(title="Vali ruudu värv")[1]  # annab hex väärtuse
                if uus_varv:
                    # Uuenda lõuendil ruudu värv
                    self.canvas.itemconfig(valitud_ruut, fill=uus_varv)

                    # Uuenda sõnastikus värv
                    taustafunktsioonid.muuda_varvi(sonastik, el, uus_varv)
                    break

        # Värskenda sõnastiku kuvamist
        self.uuenda_sonastiku_puu()


    # Sellega avaneb uus aken, kus on palju võimalusi info sisestamiseks
    def andme_dialog(self, punkti_nimi):
        andmete_aken = tk.Toplevel(self.root)
        andmete_aken.title('Andmete muutmine')

        andmete_aken.attributes('-topmost', True) # Teeb nii, et aken oleks kõige ülemine

        tk.Label(andmete_aken, text="Nimi:").grid(row=0, column=0, padx=5, pady=5)
        nimi_var = tk.Entry(andmete_aken)
        nimi_var.insert(0, sonastik[punkti_nimi].get("nimi", ""))
        nimi_var.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Grupp:").grid(row=1, column=0, padx=5, pady=5)
        grupp_var = tk.Entry(andmete_aken)
        grupp_var.insert(0, sonastik[punkti_nimi].get("grupp", ""))
        grupp_var.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Elektrikapp:").grid(row=2, column=0, padx=5, pady=5)
        kapp_var = tk.StringVar()
        kapp_valikud = [""] + [sonastik[k]["nimi"] for k in sonastik if k.startswith("kapp")]
        kapp_menu = ttk.Combobox(andmete_aken, textvariable=kapp_var, values=kapp_valikud)
        kapp_menu.set(sonastik[punkti_nimi].get("kapp", ""))
        kapp_menu.grid(row=2, column=1, padx=5, pady=5)

        # Seadmed ja vooluvajadus
        tk.Label(andmete_aken, text="Seadmed ja nende vool (W):").grid(row=3, column=0, padx=5, pady=5)
        seadmed = sonastik[punkti_nimi].get("seadmed", {})

        # Seadmete haldamise raamistik
        seadmete_raam = tk.Frame(andmete_aken)
        seadmete_raam.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Kommenteermine ja selle raam
        kommenteerimise_raam = tk.Frame(andmete_aken, width=300, height=300)
        tk.Label(andmete_aken, text="Kommentaarid:").grid(row=5, column=0, padx=5, pady=5)
        kommenteerimise_raam.grid(row=6, columnspan=2)
        kommenteerimine_var = tk.Text(kommenteerimise_raam, wrap="word", width=40, height=20)
        kommenteerimine_var.insert("1.0", sonastik[punkti_nimi].get("kommentaar", ""))
        kommenteerimine_var.grid(row=0, column=0, padx=5, pady=5)

        # Andme dialoogi salvestamisel kaasatakse ka kommenteerimine
        def kommenteerimine():
            return kommenteerimine_var.get("1.0", 'end-1c')


        def uuenda_seadmete_loend():
            """Uuendab seadmete nimekirja kuvamist."""
            for seade in seadmete_raam.winfo_children():
                seade.destroy()

            # Arvutab seadmete arvu
            for idx, (seade, vool) in enumerate(seadmed.items()):
                tk.Label(seadmete_raam, text=f"{seade}:").grid(row=idx, column=0, sticky="w", padx=5, pady=2)
                vool_var = tk.Entry(seadmete_raam, width=10)
                vool_var.insert(0, str(vool)) # Sisestab, kui palju voolu seade võtab
                vool_var.grid(row=idx, column=1, padx=5, pady=2) # Suurendab ridade arvu sõltuvalt seadmete arvust


                def salvesta_seadme_vool(nimi=seade, voolu_var=vool_var):
                    try:
                        seadmed[nimi] = int(voolu_var.get())
                    except ValueError:
                        messagebox.showerror("Viga", "Palun sisesta korrektne number.") # Juhul, kui sisestada näiteks tähti või kui ei ole määratud seadmele nime

                tk.Button(seadmete_raam, text="Muuda", command=salvesta_seadme_vool).grid(row=idx, column=2, padx=5,
                                                                                          pady=2) # Salvestab seadme voolu sõnasikku

                def eemalda_seade(nimi=seade):
                    del seadmed[nimi]
                    uuenda_seadmete_loend()

                tk.Button(seadmete_raam, text="Eemalda", command=eemalda_seade).grid(row=idx, column=3, padx=5, pady=2)

        uuenda_seadmete_loend()

        # Tekitab kõige peale akna, kus seadmeid lisada
        def lisa_seade():
            seade_aken = tk.Toplevel(andmete_aken)
            seade_aken.title("Lisa uus seade")

            seade_aken.attributes('-topmost', True)

            tk.Label(seade_aken, text="Seadme nimi:").grid(row=0, column=0, padx=5, pady=5)
            seade_nimi_var = tk.Entry(seade_aken)
            seade_nimi_var.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(seade_aken, text="Vooluvajadus (W):").grid(row=1, column=0, padx=5, pady=5)
            seade_vool_var = tk.Entry(seade_aken)
            seade_vool_var.grid(row=1, column=1, padx=5, pady=5)


            def salvesta_seade():
                nimi = seade_nimi_var.get()
                try:
                    vool = int(seade_vool_var.get())
                    if nimi and vool > 0:
                        seadmed[nimi] = vool
                        uuenda_seadmete_loend()
                        seade_aken.destroy()
                    else:
                        messagebox.showerror("Viga", "Palun sisesta kehtiv nimi ja positiivne vooluvajadus.")
                except ValueError:
                    messagebox.showerror("Viga", "Palun sisesta korrektne number.")

            tk.Button(seade_aken, text="Salvesta", command=salvesta_seade).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(andmete_aken, text="Lisa uus seade", command=lisa_seade).grid(row=4, column=0, columnspan=2, pady=10)


        def arvuta_summa():
            return sum(seadmed.values())


        def salvesta_andmed():
            # Kapiga seonduv
            vana_kapp = sonastik[punkti_nimi].get("kapp", "")
            uus_kapp = kapp_var.get()
            olemasolevad_kapid = [sonastik[k].get("nimi") for k in sonastik if k.startswith("kapp")]

            if uus_kapp and uus_kapp not in olemasolevad_kapid:
                messagebox.showerror("Viga", f"Elektrikapp '{uus_kapp}' ei eksisteeri!")
                return  # Tühista muudatus

            if vana_kapp:
                for k in sonastik:
                    if sonastik[k].get("nimi") == vana_kapp:
                        sonastik[k]["vooluvajadus"] += sonastik[punkti_nimi]["vooluvajadus"] # Taastab vanale kapile voolu, mida punkt nõudis

            if not uus_kapp:
                sonastik[punkti_nimi]['kapp'] = '' # Võimaldab eemaldada kapi nii, et ei võta uut kappi

            elif uus_kapp:
                for k in sonastik:
                    if sonastik[k].get("nimi") == uus_kapp:
                        sonastik[k]["vooluvajadus"] -= arvuta_summa() # Arvutab kapi voolust punkti voolu maha
                        sonastik[punkti_nimi]["kapp"] = uus_kapp

            # Ülejäänud andmete salvestamine
            taustafunktsioonid.muuda_nime(sonastik, punkti_nimi, nimi_var.get())
            taustafunktsioonid.muuda_gruppi(sonastik, punkti_nimi, grupp_var.get())
            taustafunktsioonid.muuda_vooluvajadust(sonastik, punkti_nimi, arvuta_summa())
            taustafunktsioonid.muuda_seadmeid(sonastik, punkti_nimi, seadmed)
            kommentaar = kommenteerimine()
            taustafunktsioonid.muuda_kommentaari(sonastik, punkti_nimi, kommentaar)
            self.uuenda_sonastiku_puu()
            self.uuenda_punktid()
            andmete_aken.destroy()


        def tühista():
            andmete_aken.destroy()

        tk.Button(andmete_aken, text="Salvesta", command=salvesta_andmed).grid(row=12, column=0, padx=5, pady=10)
        tk.Button(andmete_aken, text="Tühista", command=tühista).grid(row=12, column=1, padx=5, pady=10)


    # Näitab, mis punktid valitud kappi kuuluvad ja palju nad voolu võtavad
    def naita_kapi_punkte(self, kapp_id):
        kapi_aken = tk.Toplevel(self.root)
        kapi_aken.title(f"Punktid kapis: {sonastik[kapp_id]['nimi']}")

        tk.Label(kapi_aken, text=f"Elektrikapp: {sonastik[kapp_id]['nimi']}").pack(pady=5)

        punktide_loetelu = tk.Listbox(kapi_aken, width=50, height=15)
        punktide_loetelu.pack(padx=10, pady=10)

        for punkt_id, andmed in sonastik.items():
            if andmed.get("kapp") == sonastik[kapp_id]["nimi"]:
                punktide_loetelu.insert(tk.END, f"{andmed['nimi']} - {andmed['vooluvajadus']}W")

        tk.Button(kapi_aken, text="Sulge", command=kapi_aken.destroy).pack(pady=10)


ProgrammiGUI() # Käivitab programmi
