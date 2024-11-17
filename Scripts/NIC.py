import sys
import os
import NIC_Functions.PyNotam.notam as notam
from NIC_Functions.Hexagon_AP import generate_hexagon_for_airport

## PLACE HOLDER API REQUEST

# Ensure the NIC_Functions directory is in the Python path
base_dir = os.path.dirname(os.path.abspath(__file__))
nic_functions_dir = os.path.join(base_dir, 'NIC_Functions')
sys.path.insert(0, nic_functions_dir)

print('Welcome to NIC (NOTAMs IVAO Colombia Tool)\n')

# Menu options
select = int(input(
    '1 - Upload NOTAMs (Remember to place the .xls under the Input folder)\n'
    '2 - Select & Output NOTAMs\n'
    '3 - Other\n'
    '4 - NOTAM Parser Utility\n'
    '5 - NOTAM AP Hexagon Creator\n'
    '\n'
    'Selection: '
))

if type(select) != int:
    print('Invalid Selection')

if select == 1:
    try:
        import NIC_Functions.Update_NOTAMs
    except ImportError as e:
        print(f"Error importing Update_NOTAMs.py: {e}")

elif select == 2:
    # Prompt the user to input NOTAM LTA Codes
    user_input = input('Put here your Selected NOTAMs Code here (Use separators as [,], [;], [:], [ ]): \nInput: ')

    try:
        # Import the process_notams function from Select_Out_NOTAMs
        from NIC_Functions.Select_Out_NOTAMs import process_notams

        # Call the process_notams function directly with user input
        process_notams(user_input)

    except ImportError as e:
        print(f"Error importing Select_Out_NOTAMs.py: {e}")
    except Exception as e:
        print(f"Error processing NOTAMs: {e}")

elif select == 3:
    select_two = int(input(
        '1 - Clear <<ALL_NOTAMS>> Database\n'
        '2 - Clear <<Displayed_NOTAMS>> Database\n'
        '3 - TBD\n\n'
        'Selection: '
    ))
    if select_two == 1:
        try:
            from NIC_Functions.Clear_ALL_NOTAMs import clear_database
            clear_database()  # Call the function explicitly
        except ImportError as e:
            print(f"Error importing Clear_ALL_NOTAMs.py: {e}")

elif select == 4:
    # Get NOTAM_LTA_Number from user
    notam_lta_number = input("Enter the NOTAM_LTA_Number to retrieve: ")

    try:
        from NIC_Functions.NOTAM_Parser import get_notam_condition_subject_title, decode_notam

        # Retrieve the NOTAM Condition Subject Title
        notam_title = get_notam_condition_subject_title(notam_lta_number)
        print(f"--- Raw NOTAM ---:\n{notam_title}")

        # Decode the NOTAM
        decoded_notam = decode_notam(notam_title)

        # Print the decoded result
        print("\n--- Decoded NOTAM ---")
        print(f"NOTAM {decoded_notam['notam_id']}")
        print(f"Affects: {decoded_notam['location']}")
        print(f"From: {decoded_notam['valid_from']}")
        print(f"To: {decoded_notam['valid_until']}")
        print("Description:")
        print(f"{decoded_notam['description']}")
        print(f"{decoded_notam['level_res']}")


    except ImportError as e:
        print(f"Error importing NOTAM_Parser.py: {e}")
    except Exception as e:
        print(f"Error processing NOTAM: {e}")

elif select == 5:
    # NOTAM AP Hexagon Creator
    icao_code = input("Enter the ICAO code of the airport: ").strip().upper()
    try:
        # Prompt for radius if needed
        radius_nm = input("Enter the radius in NM for the hexagon (default 15NM): ").strip()
        radius_nm = float(radius_nm) if radius_nm else 15.0

        # Call the function to generate the hexagon
        hexagon_file = generate_hexagon_for_airport(
            icao_code=icao_code,
            output_dir=os.path.join(base_dir, "Output"),  # resource_dir removed
            radius_nm=radius_nm
        )

        print(f"Hexagon coordinates saved to {hexagon_file}")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

