import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
import peaprogramm

punkti_loendur = 1
class programmi_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1800x1000")
        self.root.title("Koordinaatide valimine")
        self.labels_dict = {}


        # menu lisamine
        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=exit)
        self.filemenu.add_command(label='Faili nimi', command=vali_fail)

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

        # Tekitab GUIsse tabeli punktidega
        self.tabel = tk.Frame(self.root)
        self.tabel.place(relx=0.8, rely=0.1)

        self.root.mainloop()

def lisa_nimekirja(self, punkti_nimi):
    global GUI_nimekiri
    # loob punkti GUI tabelisse
    punkt_tabelis = tk.Label(self.tabel, text=punkti_nimi)
    punkt_tabelis.pack(pady=5, anchor="w")
    self.labels_dict[punkti_nimi] = punkt_tabelis


def lisa_ruut(self, event):
    global punkti_loendur
    x, y = event.x, event.y  # Koordinaadid, kuhu hiirega vajutati
    suurus = 10  # Ruudu suurus pikslites
    värv = "red"  # Ruudu värv

    # Joonista punkt (ruut) klikitud kohta
    self.canvas.create_rectangle(
        x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2, fill=värv, outline="black"
    )

    punkti_nimi = 'punkt-' + str(punkti_loendur)
    peaprogramm.lisa_sonastikku(sonastik, punkti_nimi)

    # Kutsume andme dialoogi
    andme_dialog(self, punkti_nimi, (x, y))

    # Lisame punkti GUIsse
    lisa_nimekirja(self, punkti_nimi)

    punkti_loendur += 1




def eemalda_ruut(self, event):
    # Leia objekt ruudul, millele paremklõps tehti (arvutab ruudu, mille järel arvutab kohe ruudu keskme)
    kustutatav = self.canvas.find_closest(event.x, event.y)[0]
    vajutatud_punkt = self.canvas.coords(kustutatav)
    punktikese_x = (vajutatud_punkt[0] + vajutatud_punkt[2]) / 2
    punktikese_y = (vajutatud_punkt[1] + vajutatud_punkt[3]) / 2
    punktikese = (punktikese_x, punktikese_y)
    try:
        for el in sonastik:
            if el.startswith('punkt') and punktikese == sonastik[el]["koordinaat"]:
                if messagebox.askyesno(title='Kustuta?', message=f'Kas oled kindel, et soovid {sonastik[el]["nimi"]} eemaldada?'):
                    # Eemalda ruut lõuendilt, sõnastikust ja GUI tablist
                    self.canvas.delete(kustutatav)
                    print(f"Ruut on eemaldatud asukohast: x={sonastik[el]['koordinaat'][0]}, y={sonastik[el]['koordinaat'][1]}")
                    del sonastik[el]
                    if el in self.labels_dict:
                        label = self.labels_dict[el]
                        label.destroy()
                        del self.labels_dict[el]
                    break

    except:
        print("Sõnastik läbitud")
        print(sonastik)



def andme_dialog(self, punkti_nimi, coords):
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
        peaprogramm.muuda_nime(sonastik, punkti_nimi, nimi_var.get())
        peaprogramm.muuda_koordinaate(sonastik, punkti_nimi, coords)
        peaprogramm.muuda_gruppi(sonastik, punkti_nimi, grupp_var.get())
        peaprogramm.muuda_vooluvajadust(sonastik, punkti_nimi, int(vooluvajadus_var.get()) if vooluvajadus_var.get().isdigit() else 0)
        peaprogramm.muuda_kommentaari(sonastik, punkti_nimi, kommentaar_var.get())
        andmete_aken.destroy()  # Sulgeb akna pärast salvestamist
        print(sonastik)

    tk.Button(andmete_aken, text="Salvesta", command=salvesta_andmed).grid(row=4, column=0, columnspan=2, pady=10)


def vali_fail():
    global failinimi
    failinimi = tk.simpledialog.askstring('Failinimi', 'Sisesta failinimi: ')
    print(failinimi)







failinimi = ''
sonastik = {}
programmi_GUI()
