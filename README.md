# NOTAMs IVAO Colombia

This is the repository for the Colombian Division NOTAM system. Where it's feeded manually and automatically fetched into our database where NOTAMs that enhance simulation are selected for deploy at IVAO. 

This tool helps ATC Ops staff to make this process easier.

The following list includes the airports we are fetching NOTAMs from our source:

```text
SKED, SKEC, SKBO, SKRG, SKCG, SKCL, SKBQ, SKSP, SKSM, SKPE, SKBG, SKMD, SKMR, SKCC, SKVP, SKAR, SKUI, SKYP, SKPS, SKNV, SKLT, SKMZ, SKIB, SKLC, SKVV, SKRH, SKCO, SKEJ, SKUC, SKPP, SKFL, SKCZ, SKAS, SKPG, SKBS, SKCU, SKPD, SKMU, SKPV, SKPC, SKLM, SKNA, SKNQ, SKGP, SKVG, SKSJ, SKSA, SKPB, SKIP, SKPI, SKLG
```

## Usage
<p align="center">
  <img width="754" alt="image" src="https://github.com/user-attachments/assets/ca38ec45-4899-4b44-8d24-47ceda30deaa">
</p>

1. Run `NIC_GUI.py`
2. At first you will need to feed the database by importing a `.xls` file with the NOTAMs (see example).
3. You will have to select which NOTAMs you want to export to `Scripts/Output/Selection_Result.csv`. There you will find copy-paste solutions to integrate them on IVAO's Database.

> [!TIP]
> **You will end up with the following fields at the `.csv`:**
>
>| LTA_CODE | CENTER | LOCATION | StartTime   | ExpirationTime | Description                                                                                                                                                                                                                      | Polygon                                                                                                                                  |
>|----------|--------|----------|-------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
>| A2135/24 | SKEC   | SKCG     | 2409231130  | 2412232330     | --- Raw NOTAM ---<br>A2135/24 NOTAMN<br>Q) SKEC/QOBCE/IV/M/AE/000/001/1026N07530W010<br>A) SKCG B) 2409231130 C) 2412232330<br>D) 1130-2330<br>E) OBST INSTL, BACKHOE LOADER, HGT 20FT/6M, ELEV 66FT AMSL<br>COORD 102546.42N0753053.14W<br><br>--- Decoded NOTAM ---<br>NOTAM A2135/24<br>Affects: SKCG<br>From: 2024-09-23 11:30<br>To: 2024-12-23 23:30<br>Description:<br>Obstacle Installation, BACKHOE LOADER, Height 20FT/6M, Elevation 66FT AMSL<br>Coordinates 102546.42N0753053.14W | 10.69209:-75.51278<br>10.56707:-75.29258<br>10.31702:-75.29258<br>10.19199:-75.51278<br>10.31702:-75.73297<br>10.56707:-75.73297<br>10.69209:-75.51278 |

### The GUI:
1. **Landing page**
<p align="center">
  <img width="747" alt="image" src="https://github.com/user-attachments/assets/07dcd2bf-d621-4311-998f-33f965771db0">
</p>

3. **Upload NOTAMs**
   Drop only `.xls` files (see example)
<p align="center">
  <img width="302" alt="image" src="https://github.com/user-attachments/assets/f2a32709-2a1e-4654-9b5a-eeaa1017ca57">
</p>

5. **Select NOTAMs**
   
   Input a string of NOTAMs such as `A2610/24,A2497/24,A2134/24,A1743/24,A1253/24` you can use `[,]`, `[:]`, `[;]`, `[ ]` as delimiters. Those NOTAMs are the ones going to be on your output `.csv` file. When you have your selection ready, click ‹‹EXECUTE›› then ‹‹OPEN .CSV››

<p align="center">
   <img width="506" alt="image" src="https://github.com/user-attachments/assets/82013774-2dc8-469f-bf28-8a7d63ab0476">
</p>

7. **Parser - Decoder**
   
   You can decode NOTAMs individually only for the `Description` field by inputting **only** one NOTAM code.

<p align="center">
   <img width="505" alt="image" src="https://github.com/user-attachments/assets/86e34e44-d75f-4f2b-a442-1d64918d791a">
</p>

9. **Hexagon Creator**
    
   For every Airport, a Hexagon Polygon is goint to be created for every selected NOTAM, this action can be performed individually if you wish, by inputting your `ICAO` code of the airport (case-sensitive).

<p align="center">
   <img width="507" alt="image" src="https://github.com/user-attachments/assets/35139c02-0a7e-4b47-bb2a-139bcd331f9c">
</p>

11. **Other**
   This section is still under construction and only ‹‹DELETE ALL_NOTAMS›› works for now. (This will delete your NOTAMs Database)

<p align="center">
   <img width="304" alt="image" src="https://github.com/user-attachments/assets/58c831ed-9689-4268-9237-3eb19c1d8cf4">
</p>

## Instalation
This app has a GUI interface (see requirements.txt) for the necessary packages.




## About the Database
The database is stored locally on `Data/notams_database.db` and was created by using
```sql
CREATE TABLE ALL_NOTAMS (
        Location TEXT,
        NOTAM_LTA_Number TEXT,
        Class TEXT,
        Issue_Date_UTC TEXT,
        Effective_Date_UTC TEXT,
        Expiration_Date_UTC TEXT,
        NOTAM_Condition_Subject_Title TEXT
    )

CREATE TABLE Displayed_NOTAMS (
        Location TEXT,
        NOTAM_LTA_Number TEXT,
        Class TEXT,
        Issue_Date_UTC TEXT,
        Effective_Date_UTC TEXT,
        Expiration_Date_UTC TEXT,
        NOTAM_Condition_Subject_Title TEXT,
        Remark TEXT,
        POLYGON TEXT
    )
```


## Customization

> [!TIP]
> **Customization:**
>This software has been heavily optimized for the Colombian Airspace (Where Airports `Scripts\Resources\sk_airports.csv` which has been imported using the `IAB` tool.
>Also definitions about Airspace and Airports were made on the following files:
>- `Scripts/NIC_Functions/Select_Out_NOTAMs.py` : `CENTER_MAPPING`, `AIRPORTS`, `CENTER`.
>- `Scripts/Resources` : `SKED.txt`, `SKEC.txt`

### For `Select_Out_NOTAMs.py`
> [!NOTE]
> **Example of `Select_Out_NOTAMs.py`:**
>```python
>CENTER_MAPPING = {
>    'SKEC': ['SKEC', 'SKAG', 'SKBC', 'SKBQ', 'SKBR', 'SKCB', 'SKCG', 'SKCU', 'SKCV', 'SKCZ', 'SKFU', 'SKLM', 'SKMG',
>             'SKMJ', 'SKML', 'SKMP', 'SKMR', 'SKNC', 'SKOC', 'SKPB', 'SKRH', 'SKSM', 'SKSR', 'SKTB', 'SKTL', 'SKVP'],
>    'MPZL': ['SKSP'],
>    'SKED': ['SKED', 'SKAC', 'SKAD', 'SKAM', 'SKAP', 'SKAR', 'SKAS', 'SKBG', 'SKBO', 'SKBS', 'SKBU', 'SKCC', 'SKCD',
>             'SKCL', 'SKCM', 'SKCN', 'SKCO', 'SKCR', 'SKEB', 'SKEJ', 'SKFL', 'SKFR', 'SKGB', 'SKGI', 'SKGO', 'SKGP',
>             'SKGY', 'SKGZ', 'SKHA', 'SKHC', 'SKHZ', 'SKIB', 'SKIG', 'SKIP', 'SKJC', 'SKLA', 'SKLC', 'SKLG', 'SKLP',
>             'SKLT', 'SKMA', 'SKMD', 'SKME', 'SKMF', 'SKMN', 'SKMO', 'SKMU', 'SKMZ', 'SKNA', 'SKNQ', 'SKNV', 'SKOC',
>             'SKOE', 'SKOT', 'SKPA', 'SKPC', 'SKPD', 'SKPE', 'SKPG', 'SKPI', 'SKPN', 'SKPP', 'SKPQ', 'SKPR', 'SKPS',
>             'SKPZ', 'SKQU', 'SKRG', 'SKSA', 'SKSF', 'SKSG', 'SKSJ', 'SKSO', 'SKSV', 'SKTD', 'SKTI', 'SKTJ', 'SKTM',
>             'SKTQ', 'SKTU', 'SKUA', 'SKUC', 'SKUI', 'SKUL', 'SKUR', 'SKVG', 'SKVN', 'SKVV', 'SKYP', 'SQUJ']
>}
>
># Airports list for hexagon generation
>AIRPORTS = ['SKSP', 'SKAG', 'SKBC', 'SKBQ', 'SKBR', 'SKCB', 'SKCG', 'SKCU', 'SKCV', 'SKCZ', 'SKFU', 'SKLM', 'SKMG', 'SKMJ',
>            'SKML', 'SKMP', 'SKMR', 'SKNC', 'SKOC', 'SKPB', 'SKRH', 'SKSM', 'SKSR', 'SKTB', 'SKTL', 'SKVP', 'SKAC', 'SKAD',
>            'SKAM', 'SKAP', 'SKAR', 'SKAS', 'SKBG', 'SKBO', 'SKBS', 'SKBU', 'SKCC', 'SKCD', 'SKCL', 'SKCM', 'SKCN', 'SKCO',
>            'SKCR', 'SKEB', 'SKEJ', 'SKFL', 'SKFR', 'SKGB', 'SKGI', 'SKGO', 'SKGP', 'SKGY', 'SKGZ', 'SKHA', 'SKHC', 'SKHZ',
>            'SKIB', 'SKIG', 'SKIP', 'SKJC', 'SKLA', 'SKLC', 'SKLG', 'SKLP', 'SKLT', 'SKMA', 'SKMD', 'SKME', 'SKMF', 'SKMN',
>            'SKMO', 'SKMU', 'SKMZ', 'SKNA', 'SKNQ', 'SKNV', 'SKOC', 'SKOE', 'SKOT', 'SKPA', 'SKPC', 'SKPD', 'SKPE', 'SKPG',
>            'SKPI', 'SKPN', 'SKPP', 'SKPQ', 'SKPR', 'SKPS', 'SKPZ', 'SKQU', 'SKRG', 'SKSA', 'SKSF', 'SKSG', 'SKSJ', 'SKSO',
>            'SKSV', 'SKTD', 'SKTI', 'SKTJ', 'SKTM', 'SKTQ', 'SKTU', 'SKUA', 'SKUC', 'SKUI', 'SKUL', 'SKUR', 'SKVG', 'SKVN',
>            'SKVV', 'SKYP', 'SQUJ', 'SKED', 'SKEC']
>
>CENTER = ['SKEC', 'SKED']
>```

> [!CAUTION]
> See how on `CENTER_MAPPING` *Centers* are also inside the dictionary.

### At `\Script\Resources.py`
> [!NOTE]
> Some `.txt` files have to be made in order to allow `Select_Out_NOTAMs.py` to work properly. This files have to be named as the same `CENTERS` referenced above such as:
> ```python
> CENTER = ['SKEC', 'SKED']
> ```
> Examples are provided on this repository. In IVAO we might use `.pvf` files for polygons which have a format of:
> ```plaintext
> N0043150 W0825449
> N0012450 W0825459
> N0012500 W0785939
> N0043150 W0825449
> ```
> Those are in the format of `LAT LON` being:
> ```plaintext
> LAT: N0043150 -> N 004º 31' 50"
> LON: W0825449 -> W 082º 54' 49"
> ```
> Also on that directory `Scripts/Resources/coord_conv.py` there's a tool to convert coordinates from that format to *webeye's*

> [!CAUTION]
> On your `.pvf` file you have to close the polygon -The starting coordinate has to be the same at the end-

> [!CAUTION]
> The output file has to be named as the center name (Case-sensitive). SKED -> `SKED.txt`. Because this will be the polygon that is going to be on the `Scripts/Output/Selection_Result.csv` output.



Made with ❤ by [657678](http://ivao.aero/Member.aspx?Id=657678)

