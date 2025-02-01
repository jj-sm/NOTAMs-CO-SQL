import sqlite3
import os
import NIC.NIC_Functions.PyNotam.notam as notam

# Correct relative path to the database
db_path = os.path.join(os.path.dirname(__file__), '../../Data', 'notams_database.db')

def get_notam_condition_subject_title(notam_lta_number):
    """
    Retrieve the NOTAM Condition Subject Title based on the LTA number from the database.
    """
    # Check if the database file exists
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query the database for the NOTAM with the given LTA number
        cursor.execute("SELECT NOTAM_Condition_Subject_Title FROM ALL_NOTAMS WHERE NOTAM_LTA_Number = ?",
                       (notam_lta_number,))
        row = cursor.fetchone()

        # Check if the NOTAM was found
        if row:
            # Return the NOTAM condition subject title
            return row[0]
        else:
            raise ValueError(f"NOTAM with LTA number {notam_lta_number} not found.")

    except sqlite3.Error as e:
        raise Exception(f"Error connecting to SQLite database: {e}")
    finally:
        # Close the database connection
        conn.close()

def decode_notam(notam_condition_subject_title):
    """
    Decode a given NOTAM Condition Subject Title using the PyNotam library.
    """
    try:
        # Wrap the NOTAM in parentheses before decoding
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

        # Return the decoded text details
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
