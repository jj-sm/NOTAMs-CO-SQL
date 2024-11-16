import math
import csv
import os

def hexagon_coordinates(lat, lon, radius_nm):
    """Generate coordinates for a hexagon centered at (lat, lon) with a radius in NM."""
    radius_deg = radius_nm * 0.01667  # Convert NM to degrees
    vertices = []

    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)

        # Calculate the offset for each vertex
        vertex_lat = lat + radius_deg * math.cos(angle_rad)
        vertex_lon = lon + radius_deg * math.sin(angle_rad) / math.cos(math.radians(lat))

        vertices.append((vertex_lat, vertex_lon))

    # Close the hexagon by adding the first point at the end
    vertices.append(vertices[0])
    return vertices

def find_airport_coordinates(icao_code, filepath):
    """Find latitude and longitude for the given ICAO code in the CSV file."""
    with open(filepath, mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[2].strip().upper() == icao_code.upper():
                lat = float(row[5])
                lon = float(row[6])
                return lat, lon
    raise ValueError(f"ICAO code '{icao_code}' not found in {filepath}")

# Main script
try:
    ICAO = input("Enter ICAO code: ").strip()

    # Define folder paths
    resource_dir = os.path.join(os.getcwd(), "Resources")
    csv_path = os.path.join(resource_dir, "sk_airports.csv")

    output_dir = os.path.join(os.getcwd(), "Output")
    os.makedirs(output_dir, exist_ok=True)  # Create the Output directory if it doesn't exist

    lat, lon = find_airport_coordinates(ICAO, csv_path)

    # Generate hexagon with a 15 NM radius
    hexagon = hexagon_coordinates(lat, lon, 15)

    # Save coordinates in decimal format truncated to 5 decimals
    output_path_decimal = os.path.join(output_dir, f'NOTAM_hexagon_{ICAO}.txt')
    with open(output_path_decimal, 'w') as file:
        for lat, lon in hexagon:
            file.write(f"{lat:.5f}:{lon:.5f}\n")

    print(f"Coordinates saved to {output_path_decimal}")

except ValueError as e:
    print(e)
except FileNotFoundError:
    print("Error: 'airports.csv' not found in the 'Resources' directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
