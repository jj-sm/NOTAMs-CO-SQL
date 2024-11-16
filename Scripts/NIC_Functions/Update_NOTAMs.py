import os
import pandas as pd
import sqlite3
import glob

# Correct base directory: Two levels up from this script (root project directory)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Two levels up

# Correct input and database paths
input_dir = os.path.join(base_dir, 'Scripts/Input')  # Input folder relative to the project root
db_file_path = os.path.join(base_dir, 'Data', 'notams_database.db')  # Correct path to the database

# Check if the database file exists
if not os.path.exists(db_file_path):
    raise FileNotFoundError(f"The database file at {db_file_path} was not found.")

# Find the most recent .xls file in the input directory
xls_files = glob.glob(os.path.join(input_dir, 'fnsNotams_*.xls'))  # Matches files like fnsNotams_MM_DD_YYYY_HHMMSS.xls
if not xls_files:
    raise FileNotFoundError("No .xls files found in the input directory.")

# Sort the files by their modification time to get the most recent one
most_recent_file = max(xls_files, key=os.path.getmtime)

print(f"Most recent file: {most_recent_file}")

# Read the .xls file into a DataFrame, skipping the first row if it's metadata
df = pd.read_excel(most_recent_file, skiprows=4)

# Clean column names to avoid issues with spaces or formatting
df.columns = df.columns.str.strip()

# Check for the 'Location' column
if 'Location' not in df.columns:
    print("Error: 'Location' column is missing.")
    print("Available columns:", df.columns)
    exit()

# Connect to the existing SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Ensure the NOTAM_LTA_Number column is a unique identifier
# Create the ALL_NOTAMS table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS ALL_NOTAMS (
    Location TEXT,
    NOTAM_LTA_Number TEXT UNIQUE,
    Class TEXT,
    Issue_Date_UTC TEXT,
    Effective_Date_UTC TEXT,
    Expiration_Date_UTC TEXT,
    NOTAM_Condition_Subject_Title TEXT
)
''')
conn.commit()

# Initialize a counter for the added NOTAMs
notams_added = 0

# Iterate over each row in the DataFrame and insert data into the ALL_NOTAMS table
for _, row in df.iterrows():
    try:
        # Clean the NOTAM_LTA_Number to remove extra spaces and normalize case
        notam_lta_number = row['NOTAM #/LTA #'].strip().upper()

        # Remove any invisible characters (non-printable characters)
        notam_lta_number = ''.join(ch for ch in notam_lta_number if ch.isprintable())

        # Check if this NOTAM_LTA_Number already exists in the database
        cursor.execute('SELECT 1 FROM ALL_NOTAMS WHERE NOTAM_LTA_Number = ?', (notam_lta_number,))
        existing_entry = cursor.fetchone()

        # If the entry doesn't exist, insert it
        if not existing_entry:
            cursor.execute('''
            INSERT INTO ALL_NOTAMS (
                Location,
                NOTAM_LTA_Number,
                Class,
                Issue_Date_UTC,
                Effective_Date_UTC,
                Expiration_Date_UTC,
                NOTAM_Condition_Subject_Title
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Location'],
                notam_lta_number,
                row['Class'],
                row['Issue Date (UTC)'],
                row['Effective Date (UTC)'],
                row['Expiration Date (UTC)'],
                row['NOTAM Condition/LTA subject/Construction graphic title']
            ))
            notams_added += 1  # Increment the counter for each successfully added NOTAM
        else:
            print(f"Duplicate NOTAM_LTA_Number {notam_lta_number} skipped.")

    except sqlite3.IntegrityError:
        # Skip any duplicate NOTAM_LTA_Number entries (handled by the manual check)
        print(f"Duplicate NOTAM_LTA_Number {row['NOTAM #/LTA #']} skipped.")

# Commit the transaction and close the connection
conn.commit()
conn.close()

print(f"Database population complete. {notams_added} NOTAM(s) added.")
