import sys
import os
import NIC_Functions.PyNotam.notam as notam

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
    '\n'
    'Selection: '
))

if select == 1:
    try:
        import NIC_Functions.Update_NOTAMs
    except ImportError as e:
        print(f"Error importing Update_NOTAMs.py: {e}")

elif select == 2:
    try:
        import NIC_Functions.Select_Out_NOTAMs
    except ImportError as e:
        print(f"Error importing Select_Out_NOTAMs.py: {e}")

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
        from NIC_Functions.NOTAM_Parser import get_notam_condition_subject_title

        # Retrieve and print the NOTAM Condition Subject Title
        notam_title = get_notam_condition_subject_title(notam_lta_number)
        # print(f"Decoded NOTAM for {notam_lta_number}:\n{notam_title}")
    except ImportError as e:
        print(f"Error importing NOTAM_Parser.py: {e}")
