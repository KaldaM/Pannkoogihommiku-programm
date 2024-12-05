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


sonastik = {
    'kapid': {
            'kapp1': [11.23, 25.12],
            'kapp2': [22.0, 23.0]
        }
}


class ProgrammiGUI:
    def __init__(self):
        self.punkti_loendur = 1
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
            "Kaardile vajutades vasakklõps lisab ruudu, paremklõps eemaldab ruudu ja rullikule vajutamine muudab värvi"
        )
        self.silt = tk.Label(self.root, textvariable=self.kaardijuhis, font=("Arial", 15, "bold"))
        self.silt.pack(padx=15, pady=15, anchor="nw")

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


        # Seome sündmused, kasutades lambda't, et edasi anda `self`
        self.canvas.bind("<Button-1>", self.lisa_ruut)
        self.canvas.bind("<Button-3>", self.eemalda_ruut)
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
                suurus = 20
                # Highlight ainult valitud punkt
                self.canvas.create_rectangle(
                    koordinaadid[0] - suurus / 2, koordinaadid[1] - suurus / 2,
                    koordinaadid[0] + suurus / 2, koordinaadid[1] + suurus / 2,
                    outline="yellow", width=3, tags="highlight"
                )
                # Ava andmete muutmise dialoog
                self.andme_dialog(punkt_id, koordinaadid, punkt_data.get("värv", "#FFFFFF"))


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


    def expordi_sonastik(self):
        salvestuskoht = filedialog.askopenfilename(title='Vali fail', filetypes=[('txt failid', '*.txt'), ('All Files', '.*')])

        if salvestuskoht:
            global sonastik
            taustafunktsioonid.salvesta_faili(sonastik, salvestuskoht)

    def uuenda_punktid(self):
        # Eemalda ainult punktid, mitte highlight
        self.canvas.delete('punkt')

        # Joonista kõik punktid uuesti
        for punkt_id, andmed in sonastik.items():
            if "koordinaat" in andmed:
                x, y = andmed["koordinaat"]
                värv = andmed.get("värv", "#FF0000")
                suurus = 10
                self.canvas.create_rectangle(
                    x - suurus / 2, y - suurus / 2,
                    x + suurus / 2, y + suurus / 2,
                    fill=värv, outline="black", tags=(punkt_id, "punkt")
                )

    def lisa_ruut(self, event):
        x, y = event.x, event.y  # Koordinaadid, kuhu hiirega vajutati
        värv = "#FF0000"  # Vaikimisi punane värv
        punkti_nimi = f'punkt-{self.punkti_loendur}'

        # Lisa punkt sõnastikku
        taustafunktsioonid.lisa_sonastikku(sonastik, punkti_nimi)
        sonastik[punkti_nimi]['koordinaat'] = (x, y)
        sonastik[punkti_nimi]['värv'] = värv

        # Tee punkt kohe nähtavaks
        suurus = 10
        self.canvas.create_rectangle(
            x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2,
            fill=värv, outline="yellow", width=3, tags=(punkti_nimi, "punkt", "highlight")
        )

        # Ava andmete muutmise dialoog
        self.andme_dialog(punkti_nimi, (x, y), värv)

        self.punkti_loendur += 1

    def eemalda_ruut(self, event):
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
