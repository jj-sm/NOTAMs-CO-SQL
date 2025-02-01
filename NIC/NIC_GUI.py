import sys
import subprocess
import os
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

# Define the base path as the directory of the current file
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets" / "frame0"

UPLOAD_SCRIPT_PATH = os.path.join(BASE_PATH, "upload", "upload.py")
SELECT_SCRIPT_PATH = os.path.join(BASE_PATH, "select", "select.py")
OTHER_SCRIPT_PATH = os.path.join(BASE_PATH, "other", "other.py")
PARSER_SCRIPT_PATH = os.path.join(BASE_PATH, "parser", "parser.py")
HEXAGON_SCRIPT_PATH = os.path.join(BASE_PATH, "hexagon", "hexagon.py")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def run_script(script_path):
    python_exec = sys.executable
    print(f"Python Executable: {python_exec}")

    if getattr(sys, 'frozen', False):
        # Running from a bundled .app, use sys._MEIPASS to get the correct path
        script_abs_path = Path(sys._MEIPASS) / "Resources" / script_path
    else:
        script_abs_path = Path(script_path).resolve()

    print(f"Resolved Script Path: {script_abs_path}")

    try:
        if script_abs_path.exists():
            print(f"Running script: {script_abs_path}")
            result = subprocess.run([python_exec, str(script_abs_path)], cwd=os.path.dirname(script_abs_path), check=True, capture_output=True, text=True)
            print(f"Script output: {result.stdout}")
            print(f"Script errors: {result.stderr}")
        else:
            print(f"Error: Script not found at {script_abs_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def run_upload_script():
    run_script(UPLOAD_SCRIPT_PATH)

def run_select_script():
    run_script(SELECT_SCRIPT_PATH)

def run_other_script():
    run_script(OTHER_SCRIPT_PATH)

def run_parser_script():
    run_script(PARSER_SCRIPT_PATH)

def run_hexagon_script():
    run_script(HEXAGON_SCRIPT_PATH)

window = Tk()

window.title("NIC")
window.geometry("753x488")
window.configure(bg="#181818")

canvas = Canvas(window, bg="#181818", height=488, width=753, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

canvas.create_rectangle(0.0, 0.0, 753.0, 92.0, fill="#1300C1", outline="")
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(661.0, 46.0, image=image_image_1)
canvas.create_text(33.0, 16.0, anchor="nw", text="NIC", fill="#FFFFFF", font=("Orbitron Bold", 48 * -1))
canvas.create_text(140.0, 28.0, anchor="nw", text="NOTAM IVAO Colombia Tool", fill="#FFFFFF",
                   font=("Poppins SemiBold", 24 * -1))
canvas.create_rectangle(0.0, 92.0, 208.0, 488.0, fill="#04014C", outline="")

# Button setup
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=run_upload_script, relief="flat")
button_1.place(x=17.0, y=125.0, width=174.0, height=45.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=run_other_script, relief="flat")
button_2.place(x=17.0, y=409.0, width=174.0, height=45.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=run_parser_script, relief="flat")
button_3.place(x=17.0, y=267.0, width=174.0, height=45.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=run_hexagon_script, relief="flat")
button_4.place(x=17.0, y=338.0, width=174.0, height=45.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0, command=run_select_script, relief="flat")
button_5.place(x=17.0, y=196.0, width=174.0, height=45.0)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(480.0, 290.0, image=image_image_2)

window.resizable(False, False)
window.mainloop()
