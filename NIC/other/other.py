import sqlite3
import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

# Import the function that clears the database
from NIC.NIC_Functions.Clear_ALL_NOTAMs import clear_database_out

OUTPUT_PATH = Path(__file__).parent
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_button_3_click(entry):
    try:
        # Call the clear_database function and pass the entry to display output
        output_message = clear_database_out(entry)
        entry.delete(1.0, "end")  # Clear existing text
        entry.insert("end", output_message)  # Insert new output message
    except Exception as e:
        entry.delete(1.0, "end")
        entry.insert("end", f"An error occurred: {e}")

window = Tk()
window.title('Other Functions')

window.geometry("312x488")
window.configure(bg="#181818")

canvas = Canvas(
    window,
    bg="#181818",
    height=488,
    width=312,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    312.0,
    92.0,
    fill="#1300C1",
    outline=""
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    228.0,
    46.0,
    image=image_image_1
)

canvas.create_text(
    11.0,
    16.0,
    anchor="nw",
    text="NIC",
    fill="#FFFFFF",
    font=("Orbitron Bold", 48 * -1)
)

canvas.create_text(
    27.0,
    301.0,
    anchor="nw",
    text="Output Message:",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 16 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    156.0,
    393.0,
    image=entry_image_1
)

# Updated text color to white
entry_1 = Text(
    bd=0,
    bg="#000000",  # Background color remains black
    fg="#FFFFFF",  # Set text color to white
    highlightthickness=0
)
entry_1.place(
    x=27.0,
    y=330.0,
    width=258.0,
    height=124.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=21.0,
    y=174.0,
    width=269.0,
    height=45.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=21.0,
    y=235.0,
    width=269.0,
    height=45.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: on_button_3_click(entry_1),  # Trigger the function on button click
    relief="flat"
)
button_3.place(
    x=21.0,
    y=113.0,
    width=268.0,
    height=45.0
)

window.resizable(False, False)
window.mainloop()
