import csv
import os
from NOTAM_Parser import get_notam_condition_subject_title, decode_notam
from Hexagon_AP import generate_hexagon_for_airport_inline  # Import the inline hexagon function

# Database path for NOTAM records
db_path = os.path.join(os.path.dirname(__file__), '../../Data', 'notams_database.db')

# Center mapping based on your file reference
CENTER_MAPPING = {
    'SKEC': ['SKEC', 'SKAG', 'SKBC', 'SKBQ', 'SKBR', 'SKCB', 'SKCG', 'SKCU', 'SKCV', 'SKCZ', 'SKFU', 'SKLM', 'SKMG',
             'SKMJ', 'SKML', 'SKMP', 'SKMR', 'SKNC', 'SKOC', 'SKPB', 'SKRH', 'SKSM', 'SKSR', 'SKTB', 'SKTL', 'SKVP'],
    'MPZL': ['SKSP'],
    'SKED': ['SKED', 'SKAC', 'SKAD', 'SKAM', 'SKAP', 'SKAR', 'SKAS', 'SKBG', 'SKBO', 'SKBS', 'SKBU', 'SKCC', 'SKCD',
             'SKCL', 'SKCM', 'SKCN', 'SKCO', 'SKCR', 'SKEB', 'SKEJ', 'SKFL', 'SKFR', 'SKGB', 'SKGI', 'SKGO', 'SKGP',
             'SKGY', 'SKGZ', 'SKHA', 'SKHC', 'SKHZ', 'SKIB', 'SKIG', 'SKIP', 'SKJC', 'SKLA', 'SKLC', 'SKLG', 'SKLP',
             'SKLT', 'SKMA', 'SKMD', 'SKME', 'SKMF', 'SKMN', 'SKMO', 'SKMU', 'SKMZ', 'SKNA', 'SKNQ', 'SKNV', 'SKOC',
             'SKOE', 'SKOT', 'SKPA', 'SKPC', 'SKPD', 'SKPE', 'SKPG', 'SKPI', 'SKPN', 'SKPP', 'SKPQ', 'SKPR', 'SKPS',
             'SKPZ', 'SKQU', 'SKRG', 'SKSA', 'SKSF', 'SKSG', 'SKSJ', 'SKSO', 'SKSV', 'SKTD', 'SKTI', 'SKTJ', 'SKTM',
             'SKTQ', 'SKTU', 'SKUA', 'SKUC', 'SKUI', 'SKUL', 'SKUR', 'SKVG', 'SKVN', 'SKVV', 'SKYP', 'SQUJ']
}

# Airports list for hexagon generation
AIRPORTS = ['SKSP', 'SKAG', 'SKBC', 'SKBQ', 'SKBR', 'SKCB', 'SKCG', 'SKCU', 'SKCV', 'SKCZ', 'SKFU', 'SKLM', 'SKMG', 'SKMJ',
            'SKML', 'SKMP', 'SKMR', 'SKNC', 'SKOC', 'SKPB', 'SKRH', 'SKSM', 'SKSR', 'SKTB', 'SKTL', 'SKVP', 'SKAC', 'SKAD',
            'SKAM', 'SKAP', 'SKAR', 'SKAS', 'SKBG', 'SKBO', 'SKBS', 'SKBU', 'SKCC', 'SKCD', 'SKCL', 'SKCM', 'SKCN', 'SKCO',
            'SKCR', 'SKEB', 'SKEJ', 'SKFL', 'SKFR', 'SKGB', 'SKGI', 'SKGO', 'SKGP', 'SKGY', 'SKGZ', 'SKHA', 'SKHC', 'SKHZ',
            'SKIB', 'SKIG', 'SKIP', 'SKJC', 'SKLA', 'SKLC', 'SKLG', 'SKLP', 'SKLT', 'SKMA', 'SKMD', 'SKME', 'SKMF', 'SKMN',
            'SKMO', 'SKMU', 'SKMZ', 'SKNA', 'SKNQ', 'SKNV', 'SKOC', 'SKOE', 'SKOT', 'SKPA', 'SKPC', 'SKPD', 'SKPE', 'SKPG',
            'SKPI', 'SKPN', 'SKPP', 'SKPQ', 'SKPR', 'SKPS', 'SKPZ', 'SKQU', 'SKRG', 'SKSA', 'SKSF', 'SKSG', 'SKSJ', 'SKSO',
            'SKSV', 'SKTD', 'SKTI', 'SKTJ', 'SKTM', 'SKTQ', 'SKTU', 'SKUA', 'SKUC', 'SKUI', 'SKUL', 'SKUR', 'SKVG', 'SKVN',
            'SKVV', 'SKYP', 'SQUJ', 'SKED', 'SKEC']

CENTER = ['SKEC', 'SKED']

def get_polygon_from_center_file(location, resource_dir):
    """
    Fetch polygon data from a specific center file based on LOCATION.

    Parameters:
    location (str): The LOCATION value ('SKEC', 'SKED').
    resource_dir (str): Path to the Resources directory.

    Returns:
    str: Contents of the respective file, preserving line breaks.
    """
    # Construct the file path
    file_path = os.path.join(resource_dir, f"{location}.txt")

    # Read and return the file content
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"File not found for location {location}: {file_path}")

def extract_time(time_str, start_char):
    index_start = time_str.find(start_char)
    if index_start != -1:
        time_str = time_str[index_start + 1:].strip()
        end_index = next((i for i, char in enumerate(time_str) if char.isalpha()), len(time_str))
        time_value = time_str[:end_index].strip()
        return time_value.replace('[', '').replace(']', '').replace(')', '').replace('(', '')
    return ""


def determine_center(location):
    for center, locations in CENTER_MAPPING.items():
        if location in locations:
            return center
    return ""


def fetch_notams(lta_codes):
    notams_data = []
    for lta_code in lta_codes:
        try:
            notam_title = get_notam_condition_subject_title(lta_code)
            decoded_notam = decode_notam(notam_title)
            start_time = extract_time(notam_title, 'B)')
            expiration_time = extract_time(notam_title, 'C)')
            location = ''.join(decoded_notam['location'])
            center = determine_center(location)

            polygon = ""
            resource_dir = os.path.join(os.path.dirname(__file__), '../Resources')
            if location in AIRPORTS or location in CENTER:
                if location in ['SKEC', 'SKED']:
                    print(f"Fetching polygon for {location} from file.")
                    polygon = get_polygon_from_center_file(location, resource_dir)
                else:
                    print(f"Generating hexagon polygon for {location}.")
                    polygon = generate_hexagon_for_airport_inline(location, resource_dir=resource_dir)
                    polygon = "\n".join(polygon.split())

            description = f"--- Raw NOTAM ---\n{notam_title}\n\n--- Decoded NOTAM ---\n"
            description += f"NOTAM {decoded_notam['notam_id']}\n"
            description += f"Affects: {decoded_notam['location']}\n"
            description += f"From: {decoded_notam['valid_from']}\n"
            description += f"To: {decoded_notam['valid_until']}\n"
            description += f"Description:\n{decoded_notam['description']}\n"
            description += f"{decoded_notam['level_res']}\n"
            print(f"NOTAM {decoded_notam['notam_id']} added")

            notams_data.append({
                'LTA_CODE': lta_code,
                'CENTER': center,
                'LOCATION': location,
                'StartTime': start_time,
                'ExpirationTime': expiration_time,
                'Description': description,
                'Polygon': polygon
            })
        except Exception as e:
            print(f"Error processing NOTAM {lta_code}: {e}")
    return notams_data


def process_notams(lta_codes_input):
    lta_codes = [code.strip() for code in lta_codes_input.replace(',', ' ').replace(';', ' ').replace('\n', ' ').replace(':', ' ').split()]
    notams_data = fetch_notams(lta_codes)

    output_dir = os.path.join(os.path.dirname(__file__), '../Output')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'Selection_Result.csv')

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['LTA_CODE', 'CENTER', 'LOCATION', 'StartTime', 'ExpirationTime',
                                                  'Description', 'Polygon'], delimiter=';')
        writer.writeheader()
        writer.writerows(notams_data)

    print(f"NOTAM data written to {output_file}")

