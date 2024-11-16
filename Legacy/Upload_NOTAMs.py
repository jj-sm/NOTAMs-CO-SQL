import pandas as pd
import sqlite3
import os
import glob

# Directory paths
input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Scripts/Input')  # Relative path to input directory
db_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Data/notams_database.db')  # Ensure this is the correct path to the existing .db file

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

# Iterate over each row in the DataFrame and insert data into the ALL_NOTAMS table
for _, row in df.iterrows():
    try:
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
            row['NOTAM #/LTA #'],
            row['Class'],
            row['Issue Date (UTC)'],
            row['Effective Date (UTC)'],
            row['Expiration Date (UTC)'],
            row['NOTAM Condition/LTA subject/Construction graphic title']
        ))
    except sqlite3.IntegrityError:
        # Skip duplicate NOTAM_LTA_Number entries
        print(f"Duplicate NOTAM_LTA_Number {row['NOTAM #/LTA #']} skipped.")

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Database population complete.")
