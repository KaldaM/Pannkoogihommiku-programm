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
#
##################################################

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import taustafunktsioonid
import json

sonastik = {
    'kapid': {
            'kapp1': [11.23, 25.12],
            'kapp2': [22.0, 23.0]
        }
}
class programmi_GUI:
    def __init__(self):
        self.punkti_loendur = 1
        self.root = tk.Tk()
        self.root.geometry("1800x1000")
        self.root.title("Koordinaatide valimine")


        # menu lisamine
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=exit)
        self.filemenu.add_command(label='Impordi', command=lambda: impordi_sonastik(self))
        self.filemenu.add_command(label='Salvesta', command =expordi_sonastik)

        self.menubar.add_cascade(menu=self.filemenu, label='File')

        self.root.config(menu=self.menubar)

        # juhised kaardi kasutamiseks
        self.kaardijuhis = tk.StringVar()
        self.kaardijuhis.set(
            "Kaardile vajutades vasakklõps lisab ruudu, paremklõps eemaldab ruudu ja rullikule vajutades muudab see ruudu värvi (kui saadaval)"
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

        # Seome sündmused, kasutades lambda't, et edasi anda `self`
        self.canvas.bind("<Button-1>", lambda event: lisa_ruut(self, event))
        self.canvas.bind("<Button-3>", lambda event: eemalda_ruut(self, event))

        self.root.mainloop()


def impordi_sonastik(self):
    failitee = filedialog.askopenfilename(title='Vali fail', filetypes=[('txt failid', '*.txt'), ('All Files', '.*')])

    if failitee:
        with open(failitee, 'r', encoding='utf-8') as fail:
            andmed = json.load(fail)
            global sonastik
            sonastik.clear()
            sonastik.update(andmed)
            print('Andmed imporditud', sonastik)
            uuenda_punktid(self)


def expordi_sonastik():
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
            värv = 'red'
            self.canvas.create_rectangle(
                x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2, fill=värv, outline="black", tags=(f'punkt-{el}',"punkt")
            )


def lisa_ruut(self, event):
    x, y = event.x, event.y  # Koordinaadid, kuhu hiirega vajutati
    suurus = 10  # Ruudu suurus pikslites
    värv = "red"  # Ruudu värv

    punkti_nimi = 'punkt-' + str(self.punkti_loendur)
    # Joonista punkt (ruut) klikitud kohta
    self.canvas.create_rectangle(
        x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2, fill=värv, outline="black", tags=(punkti_nimi, 'punkt')
    )


    taustafunktsioonid.lisa_sonastikku(sonastik, punkti_nimi)

    # Kutsume andme dialoogi
    andme_dialog(self, punkti_nimi, (x, y), värv)

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
                if messagebox.askyesno(title='Kustuta?', message=f'Kas oled kindel, et soovid {sonastik[el]['nimi']} eemaldada?'):
                    # Eemalda ruut lõuendilt ja sõnastikust
                    self.canvas.delete(kustutatav)
                    print(f"Ruut on eemaldatud asukohast: x={sonastik[el]['koordinaat'][0]}, y={sonastik[el]['koordinaat'][1]}")
                    del sonastik[el]
                    break

    except:
        print("Sõnastik läbitud")
        print(sonastik)



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
        print(sonastik)

    tk.Button(andmete_aken, text="Salvesta", command=salvesta_andmed).grid(row=4, column=0, columnspan=2, pady=10)




failinimi = ''

programmi_GUI()
