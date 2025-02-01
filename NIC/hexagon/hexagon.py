from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
# Import the function to generate the hexagon coordinates
from NIC.NIC_Functions.Hexagon_AP import generate_hexagon_for_airport_inline_v2

# Path setup
OUTPUT_PATH = Path(__file__).parent
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets" / "frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# GUI Setup
window = Tk()
window.title("NOTAM Polygons")
window.geometry("515x488")
window.configure(bg="#181818")

canvas = Canvas(window, bg="#181818", height=488, width=515, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Button to generate hexagon coordinates
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0,
                  command=lambda: on_button_click(entry_1.get()), relief="flat")
button_1.place(x=22.319671630859375, y=219.0, width=194.5736541748047, height=34.38446044921875)

# Label for input ICAO
canvas.create_text(22.0, 114.0, anchor="nw", text="Input ICAO", fill="#FFFFFF", font=("Poppins SemiBold", 16 * -1))

# Input field for ICAO code
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(119.5, 176.5, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0)  # Set text color to white
entry_1.place(x=22.0, y=146.0, width=195.0, height=59.0)

# Label for output message
canvas.create_text(238.0, 114.0, anchor="nw", text="Output Message", fill="#FFFFFF", font=("Poppins SemiBold", 16 * -1))

# Output field for hexagon coordinates
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(360.5, 301.5, image=entry_image_2)
entry_2 = Text(bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0)  # Text color white
entry_2.place(x=236.0, y=146.0, width=249.0, height=309.0)

# Top bar with background color
canvas.create_rectangle(2.0, 0.0, 517.0, 92.0, fill="#1300C1", outline="")

# Logo image
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(423.0, 46.0, image=image_image_1)

# Title text
canvas.create_text(22.0, 16.0, anchor="nw", text="NIC", fill="#FFFFFF", font=("Orbitron Bold", 48 * -1))

# Disable resizing
window.resizable(False, False)


def on_button_click(icao_code):
    """Handle button click event to generate hexagon coordinates and output result."""
    try:
        # Call the function to generate hexagon coordinates for the given ICAO code
        hexagon_result = generate_hexagon_for_airport_inline_v2(icao_code)

        # Output the result in entry_2
        entry_2.delete(1.0, "end")  # Clear any previous content
        entry_2.insert("1.0", hexagon_result)  # Insert the new result

    except ValueError as e:
        entry_2.delete(1.0, "end")  # Clear any previous content
        entry_2.insert("1.0", str(e))  # Show error message if ICAO not found


# Start the GUI loop
window.mainloop()
