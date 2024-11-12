import tkinter as tk
from PIL import ImageTk,Image


sonastik = {}  # Sõnastik kuhu läheb kõiksugused punkti infod (see on tegelt peaprogrammis, aga katsetamise mõttes olen ma hetkel siia pannud)
punkti_loendur = 1
avatud_lahtrid = []  # punktide nummerdamisel




def lisa_ruut(event):
    global punkti_loendur
    x, y = event.x, event.y  # Koordinaadid, kuhu hiirega vajutati
    suurus = 10  # Ruudu suurus pikslites, mis sümboliseerib ligikaudu 3x3 meetrit
    värv = "red"  # Ruudu värv

    # Joonista punkt (ruut) klikitud kohta
    canvas.create_rectangle(x - suurus / 2, y - suurus / 2, x + suurus / 2, y + suurus / 2, fill=värv, outline="black")

    
    

    # Tekitan ajutiselt sõnastiku siia (vaheta pärast funktsiooni vastu välja)
    sonastik["punkt-" + str(punkti_loendur)] = {
        'nimi': '',
        'koordinaat': (),
        'grupp': '',
        'vooluvajadus': 0,
        'kommentaar': '',
        'värv': '',
        'vajalikud esemed': {}
    }

    # Salvestatakse punkti koordinaadid õige punkti kohale
    sonastik["punkt-" + str(punkti_loendur)]['koordinaat'] = (x, y)

    # Prindi koordinaadid konsoolis
    print(f"Punkt on lisatud asukohas: x={x}, y={y}")

    # muudetav_punkt = tk.Label(kaardiaken, text="Punkt-1", cursor="hand2") # punktide lisamist GUI tulpa, kust saab hakata punkte muutma katsetamine 
    # muudetav_punkt.pack(padx=1800, pady=20)

    punkti_loendur += 1

    print(sonastik) # sonastiku väljundi katsetamine




def eemalda_ruut(event):
    # Leia objekt ruudul, millele paremklõps tehti (arvutab ruudu, mille järel arvutab kohe ruudu keskme)
    kustutatav = canvas.find_closest(event.x, event.y)[0] 
    vajutatud_punkt = canvas.coords(kustutatav)
    punktikese_x = (vajutatud_punkt[0] + vajutatud_punkt[2]) / 2
    punktikese_y = (vajutatud_punkt[1] + vajutatud_punkt[3]) / 2
    punktikese = (punktikese_x, punktikese_y)
    try:
        for el in sonastik:
            if punktikese == sonastik[el]["koordinaat"]:
                # Eemalda ruut lõuendilt ja sõnastikust
                canvas.delete(kustutatav)
                print(f"Ruut on eemaldatud asukohast: x={sonastik[el]['koordinaat'][0]}, y={sonastik[el]['koordinaat'][1]}")
                del sonastik[el]

    except:
        print("Sõnastik läbitud")


    print(sonastik) # sonastiku väljundi katsetamine



# def muuda_värvi(event):



# peaakna tegemine
kaardiaken = tk.Tk()
kaardiaken.geometry(f"{1800}x{1000}")
kaardiaken.title("Koordinaatide valimine")



# juhised kaardi kasutamiseks
kaardijuhis = tk.StringVar()
kaardijuhis.set("Kaardile vajutades vasakklõps lisab ruudu, paremklõps eemaldab ruudu ja rullikule vajutades muudab see ruudu värvi (kui saadaval)")

silt = tk.Label(kaardiaken, textvariable=kaardijuhis, font=("Arial", 15, "bold"))
silt.pack(padx=15, pady=15, anchor="nw")



# canvase tegemine
canvas = tk.Canvas(kaardiaken, width = 1296, height = 697)
canvas.pack()
canvas.place(relx=0.01, rely=0.05, anchor="nw")

# canvasele kaardipildi panemine
kaardipilt = ImageTk.PhotoImage(Image.open("kaart.png"))
canvas.create_image(648, 348.5, image=kaardipilt)




# nupud kaardi kasutamiseks
canvas.bind("<Button-1>", lisa_ruut)  # Vasakklõps lisab ruudu
canvas.bind("<Button-3>", eemalda_ruut)  # Paremklõps eemaldab ruudu
# canvas.bind("<Button-2>", muuda_värvi)  # Keskmine klõps muudab ruudu värvi (kui saadaval)



kaardiaken.mainloop()



