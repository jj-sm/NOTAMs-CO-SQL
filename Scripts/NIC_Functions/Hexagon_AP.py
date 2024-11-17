import math
import csv
import os
from pathlib import Path

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

def generate_hexagon_for_airport(icao_code, resource_dir="Resources", output_dir="Output", radius_nm=15):
    """Main function to generate hexagon coordinates for a given ICAO code."""
    # Define file paths
    csv_path = os.path.join(resource_dir, "sk_airports.csv")
    os.makedirs(output_dir, exist_ok=True)  # Create the Output directory if it doesn't exist

    # Get airport coordinates
    lat, lon = find_airport_coordinates(icao_code, csv_path)

    # Generate hexagon coordinates
    hexagon = hexagon_coordinates(lat, lon, radius_nm)

    # Save coordinates in decimal format truncated to 5 decimals
    output_path_decimal = os.path.join(output_dir, f'NOTAM_hexagon_{icao_code}.txt')
    with open(output_path_decimal, 'w') as file:
        for lat, lon in hexagon:
            file.write(f"{lat:.5f}:{lon:.5f}\n")

    return output_path_decimal

def generate_hexagon_for_airport_inline(icao_code, resource_dir="Resources", radius_nm=15):
    """Generate hexagon coordinates as a formatted string for direct insertion."""
    # Define file paths
    csv_path = os.path.join(resource_dir, "sk_airports.csv")

    # Get airport coordinates
    lat, lon = find_airport_coordinates(icao_code, csv_path)

    # Generate hexagon coordinates
    hexagon = hexagon_coordinates(lat, lon, radius_nm)

    # Format coordinates as a string
    hexagon_str = " ".join(f"{lat:.5f}:{lon:.5f}" for lat, lon in hexagon)
    return hexagon_str


def generate_hexagon_for_airport_inline_v2(icao_code):
    """Generate hexagon coordinates as a formatted string for direct insertion."""
    # Define the absolute path to the CSV file
    csv_path = Path(__file__).resolve().parent.parent / "Resources" / "sk_airports.csv"

    # Ensure the file exists
    if not csv_path.exists():
        raise FileNotFoundError(f"The file {csv_path} does not exist!")

    # Get airport coordinates from the CSV
    lat, lon = find_airport_coordinates(icao_code, csv_path)

    # Generate hexagon coordinates with a default radius of 15 nautical miles
    radius_nm = 15
    hexagon = hexagon_coordinates(lat, lon, radius_nm)

    # Format coordinates as a string "lat:lon"
    hexagon_str = "".join(f"{lat:.5f}:{lon:.5f}\n" for lat, lon in hexagon)

    return hexagon_str