import sys
import os
import sqlite3

# Ensure the NIC_Functions directory is in the Python path
base_dir = os.path.dirname(os.path.abspath(__file__))
nic_functions_dir = os.path.join(base_dir, 'NIC_Functions')
sys.path.insert(0, nic_functions_dir)

# Import necessary functions
try:
    from NIC_Functions.NOTAM_Parser import get_notam_condition_subject_title, decode_notam
    print("Import successful!")
except Exception as e:
    print(f"Error importing NOTAM_Parser: {e}")

# Define the path to the SQLite database
db_path = os.path.join(os.path.dirname(__file__), '../Data', 'notams_database.db')

def get_notam_by_icao(icao_code):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the database for NOTAMs matching the ICAO code
    query = "SELECT * FROM ALL_NOTAMS WHERE Location LIKE ?"
    cursor.execute(query, (icao_code,))

    # Fetch all matching rows
    results = cursor.fetchall()

    conn.close()

    return results

def create_output_file():
    # Ensure Output folder exists
    output_dir = os.path.join(os.path.dirname(__file__), 'Output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return os.path.join(output_dir, 'temp_test01.txt')

def test_notam_decoding():
    # Get ICAO code from user
    icao_code = input("Enter ICAO code: ").strip()

    # Get NOTAMs for the given ICAO code
    notam_data = get_notam_by_icao(icao_code)

    # Open the output file for writing
    output_file = create_output_file()
    with open(output_file, 'w') as file:
        if notam_data:
            # Iterate through the results and process each NOTAM
            for row in notam_data:
                location, notam_lta_number, class_type, issue_date_utc, effective_date_utc, expiration_date_utc, notam_condition_subject_title = row
                file.write(f"\nProcessing NOTAM for ICAO: {icao_code} - LTA Number: {notam_lta_number}\n")

                # Retrieve the NOTAM Condition Subject Title
                notam_title = get_notam_condition_subject_title(notam_lta_number)
                file.write(f"--- Raw NOTAM ---:\n{notam_title}\n")

                # Decode the NOTAM with error handling
                try:
                    decoded_notam = decode_notam(notam_title)
                    # Write the decoded result to the text file
                    file.write(f"\n--- Decoded NOTAM ---\n")
                    file.write(f"NOTAM {decoded_notam['notam_id']}\n")
                    file.write(f"Affects: {decoded_notam['location']}\n")
                    file.write(f"From: {decoded_notam['valid_from']}\n")
                    file.write(f"To: {decoded_notam['valid_until']}\n")
                    file.write(f"Description:\n{decoded_notam['description']}\n")
                    file.write(f"{decoded_notam['level_res']}\n")
                    file.write("\n" + "=" * 40 + "\n")
                except Exception as e:
                    # Write the error into the file instead of stopping the process
                    file.write(f"\n--- Error Decoding NOTAM ---\n")
                    file.write(f"Error decoding NOTAM {notam_lta_number}: {e}\n")
                    file.write("\n" + "=" * 40 + "\n")
        else:
            file.write(f"No NOTAMs found for ICAO: {icao_code}\n")

    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    # Run the test
    test_notam_decoding()
