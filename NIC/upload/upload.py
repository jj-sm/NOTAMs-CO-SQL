import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinterdnd2 import TkinterDnD, DND_FILES
import shutil
import os

# Paths
OUTPUT_PATH = Path(__file__).parent
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets" / "frame0"
INPUT_DIR = BASE_PATH.parent.parent / "Scripts" / "Input"  # Relative path

# Ensure the input directory exists
INPUT_DIR.mkdir(parents=True, exist_ok=True)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Initialize the TkinterDnD window
window = TkinterDnD.Tk()
window.title('Upload NOTAMs')

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

# Drop zone rectangle
drop_rectangle = canvas.create_rectangle(
    27.0,
    120.0,
    285.0,
    267.0,
    fill="#003669",
    outline=""
)

canvas.create_text(
    27.0,
    302.0,
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

entry_1 = Text(
    bd=0,
    bg="#000000",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=27.0,
    y=330.0,
    width=258.0,
    height=124.0
)

# noinspection PyInterpreter
canvas.create_text(
    58.0,
    207.0,
    anchor="nw",
    text="Drop your .xls files here",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 16 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    153.0,
    180.0,
    image=image_image_2
)

def run_update(entry_1):
    """Run update_NOTAMs.py and capture its output."""
    # Run the script and capture its output
    process = subprocess.Popen(
        ['python3', str(BASE_PATH.parent.parent / 'Scripts' / 'NIC_Functions' / 'Update_NOTAMs.py')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Read the output and error streams
    stdout, stderr = process.communicate()

    # Insert the standard output into the Text widget
    if stdout:
        entry_1.insert("1.0", stdout)

    # Insert any error messages into the Text widget
    if stderr:
        entry_1.insert("1.0", f"Error: {stderr}")

def handle_drop(event):
    """Handle dropped files."""
    dropped_files = window.tk.splitlist(event.data)
    for file_path in dropped_files:
        if file_path.endswith('.xls'):
            try:
                # Copy the file to the input directory
                destination = INPUT_DIR / os.path.basename(file_path)
                shutil.copy(file_path, destination)
                entry_1.insert('end', f"File saved: {destination}\n")

                # Run the update_NOTAMs.py script and capture the output
                run_update(entry_1)
            except Exception as e:
                entry_1.insert('end', f"Error saving file: {e}\n")
        else:
            entry_1.insert('end', f"Unsupported file type: {file_path}\n")

# Enable the drop zone
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', handle_drop)
window.resizable(False, False)
window.mainloop()
