import tkinter as tk

# Loo Tkinter aken
root = tk.Tk()
root.title("Punktide lisamine, eemaldamine ja värvi muutmine")
root.geometry("1000x700")

# Laadi kaardi pilt lõuendile
image_path = "kaart.png"  # Laadi üles oma pilt
map_image = tk.PhotoImage(file=image_path)

# Loo Canvas, kus kaarti ja ruute kuvada
canvas = tk.Canvas(root, width=map_image.width(), height=map_image.height())
canvas.pack()

# Kuva kaardi pilt lõuendil
canvas.create_image(0, 0, anchor=tk.NW, image=map_image)

# Sõnastik punktide jälgimiseks (ID: koordinaadid)
points = {}


# Funktsioon ruudu loomiseks klikitud koordinaatidel
def add_square(event):
    x, y = event.x, event.y  # Koordinaadid, kuhu hiirega vajutati
    size = 10  # Ruudu suurus pikslites, sümboliseerib ligikaudu 3x3 meetrit
    color = "red"  # Ruudu värv

    # Joonista ruut (rectangle) klikitud kohta
    square_id = canvas.create_rectangle(x - size / 2, y - size / 2, x + size / 2, y + size / 2, fill=color,
                                        outline="black")

    # Salvesta ruudu ID ja koordinaadid
    points[square_id] = (x, y)

    # Prindi koordinaadid konsoolile
    print(f"Ruut lisatud asukohas: x={x}, y={y}")


# Funktsioon ruudu eemaldamiseks, kui parema klõpsuga klikitakse olemasolevale ruudule
def remove_square(event):
    # Leia objekt ruudul, millele paremklõps tehti
    clicked_item = canvas.find_closest(event.x, event.y)
    if clicked_item and clicked_item[0] in points:
        # Eemalda ruut lõuendilt ja sõnastikust
        canvas.delete(clicked_item[0])
        print(f"Ruut eemaldatud asukohast: x={points[clicked_item[0]][0]}, y={points[clicked_item[0]][1]}")
        del points[clicked_item[0]]


# Funktsioon ruudu värvi muutmiseks, kui keskmise klõpsuga klikitakse olemasolevale ruudule
def change_color(event):
    # Leia objekt ruudul, millele keskmine klõps tehti
    clicked_item = canvas.find_closest(event.x, event.y)
    if clicked_item and clicked_item[0] in points:
        # Muuda ruudu värvi
        current_fill = canvas.itemcget(clicked_item[0], "fill")
        new_color = "blue" if current_fill == "red" else "red"  # Vaheta värv
        canvas.itemconfig(clicked_item[0], fill=new_color)
        print(
            f"Ruut värv muudetud asukohas: x={points[clicked_item[0]][0]}, y={points[clicked_item[0]][1]}, uus värv: {new_color}")


# Seosta hiireklikk ruudu lisamise, eemaldamise ja värvi muutmise funktsioonidega
canvas.bind("<Button-1>", add_square)  # Vasak klõps lisab ruudu
canvas.bind("<Button-3>", remove_square)  # Parem klõps eemaldab ruudu
canvas.bind("<Button-2>", change_color)  # Keskmine klõps muudab ruudu värvi (kui saadaval)

# Käivita Tkinter'i peatsükkel
root.mainloop()
