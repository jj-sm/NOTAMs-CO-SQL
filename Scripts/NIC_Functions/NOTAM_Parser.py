import os
import sqlite3
import PyNotam.notam as notam  # Import the notam module for decoding

def get_notam_condition_subject_title(notam_lta_number: str):
    """
    Retrieve the NOTAM condition subject title for a given NOTAM_LTA_Number from the database,
    decode it using the Notam class, and return the decoded NOTAM.

    Args:
        notam_lta_number (str): The NOTAM_LTA_Number to look up.

    Returns:
        str: The decoded NOTAM condition subject title.
    """
    # Database file location
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "Data",
        "notams_database.db"
    )

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to find the NOTAM details
    cursor.execute(
        "SELECT NOTAM_Condition_Subject_Title FROM ALL_NOTAMS WHERE NOTAM_LTA_Number = ?",
        (notam_lta_number,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return f"Error: NOTAM with LTA number {notam_lta_number} not found."

    # Extract the NOTAM condition subject title
    notam_condition_subject_title = result[0]

    # Decode the NOTAM using the Notam class
    try:
        notam_obj = notam.Notam.from_str(notam_condition_subject_title)
        decoded_notam = notam_obj.decoded()  # Decoded full NOTAM text
    except Exception as e:
        conn.close()
        return f"Error decoding NOTAM: {str(e)}"

    conn.close()

    return decoded_notam
