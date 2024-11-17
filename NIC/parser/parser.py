from pathlib import Path
import sqlite3
import os
import Scripts.NIC_Functions.PyNotam.notam as notam
from tkinter import Tk, Canvas, Text, Button, PhotoImage

# Correct relative path to the database
db_path = os.path.join(os.path.dirname(__file__), '../../Data', 'notams_database.db')

OUTPUT_PATH = Path(__file__).parent
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_notam_condition_subject_title(notam_lta_number):
    """
    Retrieve the NOTAM Condition Subject Title based on the LTA number from the database.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT NOTAM_Condition_Subject_Title FROM ALL_NOTAMS WHERE NOTAM_LTA_Number = ?",
                       (notam_lta_number,))
        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            raise ValueError(f"NOTAM with LTA number {notam_lta_number} not found.")

    except sqlite3.Error as e:
        raise Exception(f"Error connecting to SQLite database: {e}")
    finally:
        conn.close()

def decode_notam(notam_condition_subject_title):
    """
    Decode a given NOTAM Condition Subject Title using the PyNotam library.
    """
    try:
        k = f"({notam_condition_subject_title})"
        w = notam.Notam.from_str(k)
        decoded_text = w.decoded().split('\n')

        new_decoded_text = []
        pos_init = None
        for i in range(len(decoded_text)):
            if str(decoded_text[i])[:2] == 'E)':
                pos_init = i
                decoded_text[i] = decoded_text[i][3:]  # Remove 'E)' part
                break
        for i in range(len(decoded_text)):
            if str(decoded_text[i])[:2] == 'F)' or str(decoded_text[i])[:2] == '(G)':
                pos_final = i
                break
            else:
                pos_final = len(decoded_text)

        for i in range(pos_init, pos_final):
            new_decoded_text.append(decoded_text[i])

        if w.valid_till == 'Permanent':
            perm = 'Permanent'
        else:
            perm = ''

        if 'EST' in str(w.valid_till):
            est = 'Estimated'
            minus = -13
        else:
            est = ''
            minus = -9

        if w.limit_lower != None and w.limit_upper != None:
            level_res_string = f'Upper Limit: {w.limit_upper}\nLower Limit: {w.limit_lower}'
        else:
            level_res_string = ''

        return {
            'notam_id': w.notam_id,
            'location': ''.join(w.location),
            'valid_from': str(w.valid_from)[:-9],
            'valid_until': str(w.valid_till)[:minus] + perm + ' ' + est,
            'description': "\n".join(new_decoded_text),
            'level_res' : level_res_string
        }

    except Exception as e:
        raise Exception(f"Error decoding the NOTAM: {e}")

# GUI Setup
window = Tk()
window.geometry("515x488")
window.configure(bg = "#181818")

canvas = Canvas(window, bg = "#181818", height = 488, width = 515, bd = 0, highlightthickness = 0, relief = "ridge")
canvas.place(x = 0, y = 0)

# Button and entry setup
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_button_click(entry_1.get("1.0", "end-1c")), relief="flat")
button_1.place(x=22.319671630859375, y=219.0, width=194.5736541748047, height=34.38446044921875)

canvas.create_text(22.0, 114.0, anchor="nw", text="Input NOTAM Code", fill="#FFFFFF", font=("Poppins SemiBold", 16 * -1))

# Switch Entry to Text widget for input
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(119.5, 176.5, image=entry_image_1)
entry_1 = Text(bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0, wrap="word")  # Set text color to white
entry_1.place(x=22.0, y=146.0, width=195.0, height=59.0)

canvas.create_text(238.0, 114.0, anchor="nw", text="Output Message", fill="#FFFFFF", font=("Poppins SemiBold", 16 * -1))

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(360.5, 301.5, image=entry_image_2)
entry_2 = Text(bd=0, bg="#000000", fg="#FFFFFF", highlightthickness=0)  # Set text color to white
entry_2.place(x=236.0, y=146.0, width=249.0, height=309.0)

canvas.create_rectangle(2.0, 0.0, 517.0, 92.0, fill="#1300C1", outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(423.0, 46.0, image=image_image_1)

canvas.create_text(17.0, 16.0, anchor="nw", text="NIC", fill="#FFFFFF", font=("Orbitron Bold", 48 * -1))

# Function to handle the button click event
def on_button_click(notam_lta_number):
    try:
        # Fetch raw NOTAM data from the database
        notam_raw = get_notam_condition_subject_title(notam_lta_number)

        # Decode the NOTAM
        notam_decoded = decode_notam(notam_raw)

        # Prepare the output string
        output_message = f"--- Raw NOTAM ---\n{notam_raw}\n\n--- Decoded NOTAM ---\n"
        output_message += f"NOTAM ID: {notam_decoded['notam_id']}\n"
        output_message += f"Location: {notam_decoded['location']}\n"
        output_message += f"Valid From: {notam_decoded['valid_from']}\n"
        output_message += f"Valid Until: {notam_decoded['valid_until']}\n"
        output_message += f"Description:\n{notam_decoded['description']}\n"
        if notam_decoded['level_res']:
            output_message += f"Level/Restriction:\n{notam_decoded['level_res']}\n"

        # Display the output message in entry_2
        entry_2.delete(1.0, "end")
        entry_2.insert("end", output_message)
    except Exception as e:
        entry_2.delete(1.0, "end")
        entry_2.insert("end", f"Error: {e}")

window.resizable(False, False)
window.mainloop()
