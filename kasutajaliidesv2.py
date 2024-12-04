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

        self.root.mainloop()

    def uuenda_sonastiku_puu(self):
        # Tühjenda eelnev TreeView
        self.tree.delete(*self.tree.get_children())

        for grupp, andmed in sonastik.items():
            # Lisa grupid (nt kapid, punktid jne)
            grupp_id = self.tree.insert("", "end", text=grupp, open=True)
            if isinstance(andmed, dict):
                for punkt, detailid in andmed.items():
                    if isinstance(detailid, dict):
                        punkt_tekst = f"{punkt} - Vool: {detailid.get('vooluvajadus', 0)}A"
                        punkt_id = self.tree.insert(grupp_id, "end", text=punkt_tekst)

                        # Lisa värvi-indikaator
                        varv = detailid.get('värv', '#FFFFFF')
                        self.tree.item(punkt_id, tags=(varv,))
        # Lisa värvi-stiilid
        self.tree.tag_configure("#FF0000", background="#FFCCCC")  # Punane
        self.tree.tag_configure("#00FF00", background="#CCFFCC")  # Roheline
        self.tree.tag_configure("#0000FF", background="#CCCCFF")  # Sinine


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
        self.canvas.delete('punkt')
        for el in sonastik:
            if el.startswith('punkt') and 'koordinaat' in sonastik[el]:
                x, y = sonastik[el]['koordinaat']
                suurus = 10
                värv = sonastik[el].get('värv', "#FF0000")  # Kasuta sõnastikust leitavat värvi või vaikimisi punast
                self.canvas.create_rectangle(
                    x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2,
                    fill=värv, outline="black", tags=(f'punkt-{el}', "punkt")
                )

        self.uuenda_sonastiku_puu()

    def lisa_ruut(self, event):
        x, y = event.x, event.y  # Koordinaadid, kuhu hiirega vajutati
        suurus = 10  # Ruudu suurus pikslites
        värv = "#FF0000"  # Ruudu värv, punane

        punkti_nimi = 'punkt-' + str(self.punkti_loendur)
        # Joonista punkt (ruut) klikitud kohta
        self.canvas.create_rectangle(
            x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2, fill=värv, outline="black", tags=(punkti_nimi, 'punkt')
        )


        taustafunktsioonid.lisa_sonastikku(sonastik, punkti_nimi)

        # Kutsume andme dialoogi
        self.andme_dialog(punkti_nimi, (x, y), "#FF0000")

        self.punkti_loendur += 1


    def eemalda_ruut(self, event):
        # Leia objekt ruudul, millele paremklõps tehti (arvutab ruudu, mille järel arvutab kohe ruudu keskme)
        kustutatav = self.canvas.find_closest(event.x, event.y)[0]
        vajutatud_punkt = self.canvas.coords(kustutatav)
        punktikese_x = (vajutatud_punkt[0] + vajutatud_punkt[2]) / 2
        punktikese_y = (vajutatud_punkt[1] + vajutatud_punkt[3]) / 2
        punktikese = (int(punktikese_x), int(punktikese_y))
        try:
            for el in sonastik:
                if el.startswith('punkt') and punktikese == tuple(sonastik[el]["koordinaat"]):
                    if messagebox.askyesno(title='Kustuta?', message=f"Kas oled kindel, et soovid {sonastik[el]['nimi']} eemaldada?"):
                        # Eemalda ruut lõuendilt ja sõnastikust
                        self.canvas.delete(kustutatav)
                        print(f"Ruut on eemaldatud asukohast: x={sonastik[el]['koordinaat'][0]}, y={sonastik[el]['koordinaat'][1]}")
                        del sonastik[el]
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
        andmete_aken.title('Sisesta andmed')

        # Loome sildid ja sisestusväljad
        tk.Label(andmete_aken, text="Nimi:").grid(row=0, column=0, padx=5, pady=5)
        nimi_var = tk.Entry(andmete_aken)
        nimi_var.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Grupp:").grid(row=1, column=0, padx=5, pady=5)
        grupp_var = tk.Entry(andmete_aken)
        grupp_var.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Vooluvajadus:").grid(row=2, column=0, padx=5, pady=5)
        vooluvajadus_var = tk.Entry(andmete_aken)
        vooluvajadus_var.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(andmete_aken, text="Kommentaar:").grid(row=3, column=0, padx=5, pady=5)
        kommentaar_var = tk.Entry(andmete_aken)
        kommentaar_var.grid(row=3, column=1, padx=5, pady=5)

        def salvesta_andmed():
            taustafunktsioonid.muuda_nime(sonastik, punkti_nimi, nimi_var.get())
            taustafunktsioonid.muuda_koordinaate(sonastik, punkti_nimi, coords)
            taustafunktsioonid.muuda_varvi(sonastik, punkti_nimi, varv)
            taustafunktsioonid.muuda_gruppi(sonastik, punkti_nimi, grupp_var.get())
            taustafunktsioonid.muuda_vooluvajadust(sonastik, punkti_nimi, int(vooluvajadus_var.get()) if vooluvajadus_var.get().isdigit() else 0)
            taustafunktsioonid.muuda_kommentaari(sonastik, punkti_nimi, kommentaar_var.get())
            andmete_aken.destroy()  # Sulgeb akna pärast salvestamist

            self.uuenda_sonastiku_puu()
            print(sonastik)

        def tühista():
            self.canvas.delete(punkti_nimi)
            if punkti_nimi in sonastik:
                del sonastik[punkti_nimi]
            andmete_aken.destroy()

        tk.Button(andmete_aken, text='Salvesta', command=salvesta_andmed).grid(row=4, column=0, padx=5, pady=10)
        tk.Button(andmete_aken, text='Tühista', command=tühista).grid(row=4,column=1,padx=5,pady=10)



ProgrammiGUI()
