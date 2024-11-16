import sqlite3
import os
import PyNotam.notam as notam

# Example NOTAM_LTA_Number to test
notam_lta_number = 'A2396/24'

# Correct relative path to the database
db_path = os.path.join(os.path.dirname(__file__), '../../Data', 'notams_database.db')

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Database file not found: {db_path}")
else:
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
            # Extract the raw NOTAM from the database
            notam_condition_subject_title = row[0]

            # Print the raw NOTAM with correct formatting
            print(f"--- Raw NOTAM ---\n{notam_condition_subject_title}\n")

            # Decode using the notam library
            try:
                # Wrap the NOTAM in parentheses before decoding
                k = f"({notam_condition_subject_title})"
                w = notam.Notam.from_str(k)
                decoded_text = w.decoded()
                decoded_text = decoded_text[1:-1]
                print(w.valid_from)

                # Print the decoded NOTAM as the Text Description with correct formatting
                print("--- Text Description ---")
                print(f"{decoded_text}\n")

            except Exception as e:
                print(f"Error decoding the NOTAM: {e}")

        else:
            print(f"NOTAM with LTA number {notam_lta_number} not found.")

    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Close the database connection
        conn.close()
