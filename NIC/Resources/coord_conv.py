def dms_to_decimal(degrees, minutes, seconds):
    """Convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees."""
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    return decimal

def convert_coordinates(lat, lon):
    """Convert latitude and longitude from DMS to decimal format. N0043015 W0803053
    N0043150 W0825449"""
    # Parse the latitude (N/S) and longitude (E/W) values
    lat_dir = lat[0]  # N or S
    lon_dir = lon[0]  # W or E
    lat_value = lat[1:]  # 0121928 (DDMMSS)
    lon_value = lon[1:]   # 0711506 (DDMMSS) 004 30 15

    lat_deg = int(lat_value[:3])
    lat_min = int(lat_value[3:5])
    lat_sec = int(lat_value[5:])

    lon_deg = int(lon_value[:3])
    lon_min = int(lon_value[3:5])
    lon_sec = int(lon_value[5:])

    # Convert to decimal
    lat_decimal = dms_to_decimal(lat_deg, lat_min, lat_sec)
    lon_decimal = dms_to_decimal(lon_deg, lon_min, lon_sec)

    # Apply negative sign for South and West
    if lat_dir == 'S':
        lat_decimal = -lat_decimal
    if lon_dir == 'W':
        lon_decimal = -lon_decimal

    return f"{lat_decimal:.5f}:{lon_decimal:.5f}"

def process_pvf_file(input_file, output_file):
    """Process a .pvf file and convert coordinates to decimal format."""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            # Remove leading/trailing spaces and split by space
            line = line.strip()
            coords = line.split()

            if len(coords) == 2:
                lat_lon_decimal = convert_coordinates(coords[0], coords[1])

                # Write to output file
                f.write(lat_lon_decimal + '\n')

# Example usage
filename = input('Enter filename: ')
# filename = 'SKED'
input_file = f'{filename}.pvf'  # .pvf file with coordinates
output_file = f'{filename}.txt'  # Output .txt file with decimal coordinates

process_pvf_file(input_file, output_file)
