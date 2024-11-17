import sqlite3
import os


def clear_database():
    try:
        # Correct base directory: Two levels up from this script (root project directory)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Two levels up

        # Correct database path
        db_file_path = os.path.join(base_dir, 'Data', 'notams_database.db')  # Correct path to the database

        # Check if the database file exists
        if not os.path.exists(db_file_path):
            raise FileNotFoundError(f"The database file at {db_file_path} was not found.")

        print(f"Database file found at: {db_file_path}")

        # Connect to the existing SQLite database
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        # Log current data in the table (optional for debugging)
        cursor.execute('SELECT COUNT(*) FROM ALL_NOTAMS')
        row_count = cursor.fetchone()[0]
        print(f"Rows in ALL_NOTAMS before clearing: {row_count}")

        # Clear all rows from the ALL_NOTAMS table (deletes all data but keeps the table structure)
        cursor.execute('DELETE FROM ALL_NOTAMS')

        # Commit the transaction and close the connection
        conn.commit()

        # Verify if the table is cleared
        cursor.execute('SELECT COUNT(*) FROM ALL_NOTAMS')
        row_count_after = cursor.fetchone()[0]
        print(f"Rows in ALL_NOTAMS after clearing: {row_count_after}")

        conn.close()

        print("Database cleared. All NOTAMs have been deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")

def clear_database_out(entry):
    try:
        # Correct base directory: Two levels up from this script (root project directory)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Two levels up

        # Correct database path
        db_file_path = os.path.join(base_dir, 'Data', 'notams_database.db')  # Correct path to the database

        # Check if the database file exists
        if not os.path.exists(db_file_path):
            raise FileNotFoundError(f"The database file at {db_file_path} was not found.")

        # Connect to the existing SQLite database
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()

        # Log current data in the table (optional for debugging)
        cursor.execute('SELECT COUNT(*) FROM ALL_NOTAMS')
        row_count = cursor.fetchone()[0]

        # Clear all rows from the ALL_NOTAMS table (deletes all data but keeps the table structure)
        cursor.execute('DELETE FROM ALL_NOTAMS')

        # Commit the transaction and close the connection
        conn.commit()

        # Verify if the table is cleared
        cursor.execute('SELECT COUNT(*) FROM ALL_NOTAMS')
        row_count_after = cursor.fetchone()[0]
        conn.close()

        return f"Database cleared. {row_count} rows were deleted. {row_count_after} rows remaining."

    except Exception as e:
        return f"An error occurred: {e}"

# If this script is executed directly, the function will run
if __name__ == "__main__":
    clear_database()
