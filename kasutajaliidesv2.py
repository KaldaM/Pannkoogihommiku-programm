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


sonastik = {
    'kapid': {
            'kapp1': [11.23, 25.12],
            'kapp2': [22.0, 23.0]
        }
}


class ProgrammiGUI:
    def __init__(self):
        self.punkti_loendur = 1
        self.mõõdulindi_punktid = []
        self.mõõdulindi_jooned = []
        self.mõõdulindi_distantsid = []
        self.mõõdulindi_punktiloendur = 0
        self.suurus = 19.67
        self.root = tk.Tk()
        self.root.geometry("1800x1000")
        self.root.title("Koordinaatide valimine")


        # menu lisamine
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=exit)
        self.filemenu.add_command(label='Impordi', command=self.impordi_sonastik)
        self.filemenu.add_command(label='Salvesta', command =self.expordi_sonastik)

        self.menubar.add_cascade(menu=self.filemenu, label='File')

        self.root.config(menu=self.menubar)

        # juhised kaardi kasutamiseks
        self.kaardijuhis = tk.StringVar()
        self.kaardijuhis.set(
            "Kaardil punktil vajutades on võimalik punkti muuta, sama töötab ka tabeli kaudu. Kaardi all paremal on kolm nuppu. Need muudavad hiire funktsioone."
        )
        self.silt = tk.Label(self.root, textvariable=self.kaardijuhis, font=("Arial", 12, "bold"))
        self.silt.pack(padx=15, pady=12, anchor="nw")

        self.kaardijuhis2 = tk.StringVar()
        self.kaardijuhis2.set(
            """Mõõdulint: vasaku klõpsuga saab lisada mõõdulindi punkte, aga paremaga kustutad saadud tulemused (ükskõik, kus vajutades).\n
            Lisa punkte: vasaku klõpsuga lisad punkte (telgid), aga paremaga kustutad vastavad punktid (otse peale vajutades).\n
            Liiguta punkte: vasaku klõpsuga hoiad soovitud punkti peal ja lohistad.
            """
        )
        self.silt = tk.Label(self.root, textvariable=self.kaardijuhis2, font=("Arial", 12, "bold"), justify="left")
        self.silt.pack(anchor="sw", side="bottom", pady=60, padx=10)

        # canvase tegemine
        self.canvas = tk.Canvas(self.root, width=1296, height=697)
        self.canvas.pack()
        self.canvas.place(relx=0.01, rely=0.05, anchor="nw")

        # canvasele kaardipildi panemine
        self.kaardipilt = ImageTk.PhotoImage(Image.open("kaart.png"))
        self.canvas.create_image(648, 348.5, image=self.kaardipilt)

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
        self.eemaldamine_aktiivne = False
        self.valitud_punkt = None

        # Nupud punktide lisamise ja liigutamise aktiveerimiseks ning mõõdulindi funktsiooni käivitamiseks
        self.mõõdulint_nupp = tk.Button(self.root, text="Mõõdulint", command=self.aktiveeri_mõõdulint)
        self.mõõdulint_nupp.place(relx=0.59, rely=0.78, anchor="se")

        self.lisa_nupp = tk.Button(self.root, text="Lisa punkte", command=self.aktiveeri_lisamine)
        self.lisa_nupp.place(relx=0.65, rely=0.78, anchor="se")

        self.liiguta_nupp = tk.Button(self.root, text="Liiguta punkte", command=self.aktiveeri_liigutamine)
        self.liiguta_nupp.place(relx=0.72, rely=0.78, anchor="se")


        # Canvase sündmuste sidumine
        self.canvas.bind("<Button-1>", self.canvas_vasakklikk)
        self.canvas.bind("<B1-Motion>", self.lohista_punkt)
        self.canvas.bind("<ButtonRelease-1>", self.lohistamise_lopp)
        self.canvas.bind("<Button-3>", self.canvas_paremklikk)
        self.canvas.bind("<Button-2>", self.muuda_ruudu_varvi)

        self.tree.bind("<<TreeviewSelect>>", self.treeview_item_selected)

        self.root.mainloop()

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
                    self.tree.tag_configure(punkt_id, background=värv)
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


    def treeview_item_selected(self, event):
        self.canvas.delete("highlight")  # Eemalda ainult highlight kastid

        selected_item = self.tree.selection()[0]  # TreeView elemendi ID vastab punkt-ID-le
        punkt_id = selected_item  # TreeView iids vastab punkt-ID-le

        if punkt_id in sonastik:
            punkt_data = sonastik[punkt_id]
            koordinaadid = punkt_data.get("koordinaat")

            if koordinaadid:
                # Highlight ainult valitud punkt
                self.canvas.create_rectangle(
                    koordinaadid[0] - self.suurus / 2, koordinaadid[1] - self.suurus / 2,
                    koordinaadid[0] + self.suurus / 2, koordinaadid[1] + self.suurus / 2,
                    outline="purple", width=3, tags="highlight"
                )
                # Ava andmete muutmise dialoog
                self.andme_dialog(punkt_id, koordinaadid, punkt_data.get("värv", "#FFFFFF"))


    #Vasaku hiireklõpsu funktsioonid:
    def aktiveeri_mõõdulint(self):
        self.mõõdulint_aktiivne = not self.mõõdulint_aktiivne
        self.mõõdulindi_reset_aktiivne = not self.mõõdulindi_reset_aktiivne
        self.liigutamine_aktiivne = False  # Deaktiveerime liigutamise
        self.lisamine_aktiivne = False  # Deaktiveerime lisamise
        self.eemaldamine_aktiivne = False  # Deaktiveerime eemaldamise
        self.lisa_nupp.config(text="Lisa punkte")
        self.liiguta_nupp.config(text="Liiguta punkte")
        if self.mõõdulint_aktiivne:
            self.mõõdulint_nupp.config(text="Mõõdulint: Aktiivne")
        else:
            self.mõõdulint_nupp.config(text="Mõõdulint")
        self.valitud_punkt = None  # Eemaldame aktiivse valiku

    def aktiveeri_lisamine(self):
        self.lisamine_aktiivne = not self.lisamine_aktiivne
        self.eemaldamine_aktiivne = not self.eemaldamine_aktiivne
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
        self.eemaldamine_aktiivne = False  # Deaktiveerime eemaldamise
        self.mõõdulint_nupp.config(text="Mõõdulint")
        self.lisa_nupp.config(text="Lisa punkte")
        if self.liigutamine_aktiivne:
            self.liiguta_nupp.config(text="Liigutamine: Aktiivne")
        else:
            self.liiguta_nupp.config(text="Liiguta punkte")
        self.valitud_punkt = None  # Eemaldame aktiivse valiku


        def vali_punkt(self, event):
            if not self.liigutamine_aktiivne:
                return

            # Leia lähim punkt koordinaatide järgi
            valitud_id = self.canvas.find_closest(event.x, event.y)
            for punkt_id, andmed in sonastik.items():
                if "koordinaat" in andmed:
                    x, y = andmed["koordinaat"]
                    if abs(x - event.x) < 10 and abs(y - event.y) < 10:  # Kui klõps on punkti lähedal
                        self.valitud_punkt = punkt_id
                        self.highlight_punkt(x, y)
                        break


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
            return

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
            return

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
                               self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1]) / 6.536, 2
            )

            # Kuvame canvasele kahe punkti vahelise distantsi
            vahemaa_tekst = self.canvas.create_text((self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1][0] + self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1][0]) / 2,
                               ((self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur][1][1] + self.mõõdulindi_punktid[self.mõõdulindi_punktiloendur + 1][1][1]) / 2) + 15,
                               text=(vahemaa, "m"), fill="black", font=("bold", 10))

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

        # Tühjendame mõõdulindiga seotud listid, et neid saaks uue mõõdulindi loomisel kasutada
        self.mõõdulindi_punktid.clear()
        self.mõõdulindi_jooned.clear()
        self.mõõdulindi_distantsid.clear()

        # Nullime punktiloenduri
        self.mõõdulindi_punktiloendur = 0

    def highlight_ja_muuda(self, event):
        # Leia lähim punkt
        valitud_id = self.canvas.find_closest(event.x, event.y)
        for punkt_id, andmed in sonastik.items():
            if "koordinaat" in andmed:
                x, y = andmed["koordinaat"]
                if abs(x - event.x) < 10 and abs(y - event.y) < 10:  # Kui klõps on punkti lähedal
                    self.highlight_punkt(x, y)  # Highlight punkt
                    self.andme_dialog(punkt_id, (x, y), andmed.get("värv", "#FFFFFF"))  # Ava andmete dialoog
                    break


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

    def highlight_punkt(self, x, y):
        self.canvas.delete("highlight")
        self.canvas.create_rectangle(
            x - self.suurus / 2, y - self.suurus / 2, x + self.suurus / 2, y + self.suurus / 2,
            outline="purple", width=3, tags="highlight"
        )

    def expordi_sonastik(self):
        salvestuskoht = filedialog.askopenfilename(title='Vali fail', filetypes=[('txt failid', '*.txt'), ('All Files', '.*')])

        if salvestuskoht:
            global sonastik
            taustafunktsioonid.salvesta_faili(sonastik, salvestuskoht)

    def uuenda_punktid(self):
        # Eemalda kõik punktid lõuendilt
        self.canvas.delete('punkt')

        # Joonista kõik punktid uuesti sõnastikust
        for punkt_id, andmed in sonastik.items():
            if "koordinaat" in andmed:
                x, y = andmed["koordinaat"]
                värv = andmed.get("värv", "#FF0000")  # Vaikimisi punane värv

                # Joonista punkt lõuendile ja salvesta lõuendi elemendi ID
                item_id = self.canvas.create_rectangle(
                    x - self.suurus / 2, y - self.suurus / 2,
                    x + self.suurus / 2, y + self.suurus / 2,
                    fill=värv, outline="black", tags=(punkt_id, "punkt")
                )
                andmed['canvas_id'] = item_id  # Salvesta lõuendi elemendi ID

    def lisa_ruut(self, event):
        x, y = event.x, event.y
        värv = "#FF0000"  # Vaikimisi punane värv
        punkti_nimi = f'punkt-{self.punkti_loendur}'

        # Lisa punkt sõnastikku
        taustafunktsioonid.lisa_sonastikku(sonastik, punkti_nimi)
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

    def eemalda_ruut(self, event):
        if not self.eemaldamine_aktiivne:
            return

        kustutatav = self.canvas.find_closest(event.x, event.y)[0]
        vajutatud_punkt = self.canvas.coords(kustutatav)
        punktikese_x = (vajutatud_punkt[0] + vajutatud_punkt[2]) / 2
        punktikese_y = (vajutatud_punkt[1] + vajutatud_punkt[3]) / 2
        punktikese = (int(punktikese_x), int(punktikese_y))

        try:
            for punkt in list(sonastik.keys()):
                if punkt.startswith('punkt') and punktikese == tuple(sonastik[punkt]["koordinaat"]):
                    if messagebox.askyesno(title='Kustuta?', message=f"Kas oled kindel, et soovid {sonastik[punkt]['nimi']} eemaldada?"):
                        # Eemalda ruut lõuendilt ja sõnastikust
                        self.canvas.delete(kustutatav)
                        grupp = sonastik[punkt]['grupp']
                        del sonastik[punkt]

                        # Kontrolli, kas grupp on tühi, ja eemalda see
                        if grupp and grupp in sonastik:
                            grupi_punktid = [p for p in sonastik if sonastik[p].get('grupp') == grupp]
                            if not grupi_punktid:  # Kui grupis pole enam punkte
                                del sonastik[grupp]
                                print(f"Grupp {grupp} on kustutatud, sest see on tühi.")
                        break
        except:
            print("Sõnastik läbitud")
            print(sonastik)

        self.uuenda_sonastiku_puu()


    def muuda_ruudu_varvi(self, event):
        # Leia ruut, millel klikiti
        valitud_ruut = self.canvas.find_closest(event.x, event.y)[0]
        ruudu_koordinaadid = self.canvas.coords(valitud_ruut)
        punktikese_x = (ruudu_koordinaadid[0] + ruudu_koordinaadid[2]) / 2
        punktikese_y = (ruudu_koordinaadid[1] + ruudu_koordinaadid[3]) / 2
        punktikese = (int(punktikese_x), int(punktikese_y))

        # Leia vastav punkt sõnastikust
        for el in sonastik:
            if el.startswith('punkt') and punktikese == tuple(sonastik[el]["koordinaat"]):
                # Küsi uus värv
                uus_varv = askcolor(title="Vali ruudu värv")[1]  # [1] annab hex väärtuse
                if uus_varv:
                    # Uuenda lõuendil ruudu värv
                    self.canvas.itemconfig(valitud_ruut, fill=uus_varv)

                    # Uuenda sõnastikus värv
                    taustafunktsioonid.muuda_varvi(sonastik, el, uus_varv)
                    break

        # Värskenda sõnastiku kuvamist
        self.uuenda_sonastiku_puu()

    def andme_dialog(self, punkti_nimi, coords, varv):
        andmete_aken = tk.Toplevel(self.root)
        andmete_aken.title('Andmete muutmine')

        tk.Label(andmete_aken, text="Nimi:").grid(row=0, column=0, padx=5, pady=5)
        nimi_var = tk.Entry(andmete_aken)
        nimi_var.insert(0, sonastik[punkti_nimi].get("nimi", ""))
        nimi_var.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Grupp:").grid(row=1, column=0, padx=5, pady=5)
        grupp_var = tk.Entry(andmete_aken)
        grupp_var.insert(0, sonastik[punkti_nimi].get("grupp", ""))
        grupp_var.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Vooluvajadus (W):").grid(row=2, column=0, padx=5, pady=5)
        vooluvajadus_var = tk.Entry(andmete_aken)
        vooluvajadus_var.insert(0, sonastik[punkti_nimi].get("vooluvajadus", 0))
        vooluvajadus_var.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Kommentaar:").grid(row=3, column=0, padx=5, pady=5)
        kommentaar_var = tk.Entry(andmete_aken)
        kommentaar_var.insert(0, sonastik[punkti_nimi].get("kommentaar", ""))
        kommentaar_var.grid(row=3, column=1, padx=5, pady=5)

        def salvesta_andmed():
            taustafunktsioonid.muuda_nime(sonastik, punkti_nimi, nimi_var.get())
            taustafunktsioonid.muuda_gruppi(sonastik, punkti_nimi, grupp_var.get())
            taustafunktsioonid.muuda_vooluvajadust(
                sonastik, punkti_nimi, int(vooluvajadus_var.get()) if vooluvajadus_var.get().isdigit() else 0
            )
            taustafunktsioonid.muuda_kommentaari(sonastik, punkti_nimi, kommentaar_var.get())

            self.uuenda_sonastiku_puu()
            self.uuenda_punktid()  # Värskenda kaarti
            self.canvas.delete("highlight")  # Eemalda ajutine highlight
            andmete_aken.destroy()

        def tühista():
            # Ainult sulge dialoog, ära tee muudatusi ega kustuta punkti
            self.canvas.delete("highlight")  # Eemalda highlight
            andmete_aken.destroy()

        tk.Button(andmete_aken, text='Salvesta', command=salvesta_andmed).grid(row=4, column=0, padx=5, pady=10)
        tk.Button(andmete_aken, text='Tühista', command=tühista).grid(row=4, column=1, padx=5, pady=10)


ProgrammiGUI()
