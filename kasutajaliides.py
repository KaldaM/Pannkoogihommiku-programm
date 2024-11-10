import tkinter as tk
import tkintermapview

loenduri_arv = 1
koordinaatide_hulk = {}
koordinaadid = ()

def add_marker_event(coords):
    global loenduri_arv
    global koordinaadid  
    global koordinaatide_hulk                                           
    koordinaadid = coords  #KOORDINAADID
    print("Lisatud:", coords)
    punkt = "Punkt-" + str(loenduri_arv)
    ttt = kaart.set_marker(coords[0], coords[1], text=punkt)
    koordinaatide_hulk[punkt] = koordinaadid
    loenduri_arv += 1
    print(koordinaatide_hulk)

    



# peaakna tegemine
kaardiaken = tk.Tk()
kaardiaken.geometry(f"{1800}x{1000}")
kaardiaken.title("Koordinaatide valimine")

# juhised kaardi kasutamiseks
kaardijuhis = tk.StringVar()
kaardijuhis.set("Vajuta kaardi paremat hiireklõpsu ja seejärel ""Lisa punkt""")
kaardijuhisx = tk.Label(kaardiaken, textvariable=kaardijuhis, anchor=tk.SE)

# kaardi tegemine
kaart = tkintermapview.TkinterMapView(kaardiaken, width=800, height=600, corner_radius=0)
kaart.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")                          #TILE SERVERI LINK
kaart.place(x=300, y=100)
kaart.set_position(58.380189, 26.723079)
kaart.set_zoom(18)

#koordinaadi lisamine

kaart.add_right_click_menu_command(label="Lisa punkt", command=add_marker_event, pass_coords=True)



kaardiaken.mainloop()



