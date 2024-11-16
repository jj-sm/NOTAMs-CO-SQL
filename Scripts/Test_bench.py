# In another Python file

import sys
from NIC_Functions.Hexagon_AP import generate_hexagon_for_airport

def main():
    ICAO = input("Enter ICAO code: ").strip()

    try:
        output_path = generate_hexagon_for_airport(ICAO)
        print(f"Coordinates saved to {output_path}")
    except ValueError as e:
        print(e)
    except FileNotFoundError:
        print("Error: 'airports.csv' not found in the 'Resources' directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
