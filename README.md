# NOTAMs IVAO Colombia

This is the repository for the Colombian Division NOTAM system. Where it's feeded manually and automatically fetched into our database where NOTAMs that enhance simulation are selected for deploy at IVAO.

The following list includes the airports we are fetching NOTAMs from our source:

```text
SKED, SKEC, SKBO, SKRG, SKCG, SKCL, SKBQ, SKSP, SKSM, SKPE, SKBG, SKMD, SKMR, SKCC, SKVP, SKAR, SKUI, SKYP, SKPS, SKNV, SKLT, SKMZ, SKIB, SKLC, SKVV, SKRH, SKCO, SKEJ, SKUC, SKPP, SKFL, SKCZ, SKAS, SKPG, SKBS, SKCU, SKPD, SKMU, SKPV, SKPC, SKLM, SKNA, SKNQ, SKGP, SKVG, SKSJ, SKSA, SKPB, SKIP, SKPI, SKLG
```

> When selecting a NOTAM, automatically it will generate the respective Polygon file for *webeye* integration and its translated to plain text NOTAM meaning.

This app has a GUI interface (see requirements.txt) for the necessary packages.

> [!TIP] Customization:
>This software has been heavily optimized for the Colombian Airspace (Where Airports `Scripts\Resources\sk_airports.csv` which has been imported using the `IAB` tool.
>Also definitions about Airspace and Airports were made on the following files:
>- `Scripts/NIC_Functions/Select_Out_NOTAMs.py` : `CENTER_MAPPING`, `AIRPORTS`, `CENTER`.
>> [!NOTE] Example of `Select_Out_NOTAMs.py`:
>>```python
>>CENTER_MAPPING = {
>>    'SKEC': ['SKEC', 'SKAG', 'SKBC', 'SKBQ', 'SKBR', 'SKCB', 'SKCG', 'SKCU', 'SKCV', 'SKCZ', 'SKFU', 'SKLM', 'SKMG',
>>             'SKMJ', 'SKML', 'SKMP', 'SKMR', 'SKNC', 'SKOC', 'SKPB', 'SKRH', 'SKSM', 'SKSR', 'SKTB', 'SKTL', 'SKVP'],
>>    'MPZL': ['SKSP'],
>>    'SKED': ['SKED', 'SKAC', 'SKAD', 'SKAM', 'SKAP', 'SKAR', 'SKAS', 'SKBG', 'SKBO', 'SKBS', 'SKBU', 'SKCC', 'SKCD',
>>             'SKCL', 'SKCM', 'SKCN', 'SKCO', 'SKCR', 'SKEB', 'SKEJ', 'SKFL', 'SKFR', 'SKGB', 'SKGI', 'SKGO', 'SKGP',
>>             'SKGY', 'SKGZ', 'SKHA', 'SKHC', 'SKHZ', 'SKIB', 'SKIG', 'SKIP', 'SKJC', 'SKLA', 'SKLC', 'SKLG', 'SKLP',
>>             'SKLT', 'SKMA', 'SKMD', 'SKME', 'SKMF', 'SKMN', 'SKMO', 'SKMU', 'SKMZ', 'SKNA', 'SKNQ', 'SKNV', 'SKOC',
>>             'SKOE', 'SKOT', 'SKPA', 'SKPC', 'SKPD', 'SKPE', 'SKPG', 'SKPI', 'SKPN', 'SKPP', 'SKPQ', 'SKPR', 'SKPS',
>>             'SKPZ', 'SKQU', 'SKRG', 'SKSA', 'SKSF', 'SKSG', 'SKSJ', 'SKSO', 'SKSV', 'SKTD', 'SKTI', 'SKTJ', 'SKTM',
>>             'SKTQ', 'SKTU', 'SKUA', 'SKUC', 'SKUI', 'SKUL', 'SKUR', 'SKVG', 'SKVN', 'SKVV', 'SKYP', 'SQUJ']
>>}
>>
>># Airports list for hexagon generation
>>AIRPORTS = ['SKSP', 'SKAG', 'SKBC', 'SKBQ', 'SKBR', 'SKCB', 'SKCG', 'SKCU', 'SKCV', 'SKCZ', 'SKFU', 'SKLM', 'SKMG', 'SKMJ',
>>            'SKML', 'SKMP', 'SKMR', 'SKNC', 'SKOC', 'SKPB', 'SKRH', 'SKSM', 'SKSR', 'SKTB', 'SKTL', 'SKVP', 'SKAC', 'SKAD',
>>            'SKAM', 'SKAP', 'SKAR', 'SKAS', 'SKBG', 'SKBO', 'SKBS', 'SKBU', 'SKCC', 'SKCD', 'SKCL', 'SKCM', 'SKCN', 'SKCO',
>>            'SKCR', 'SKEB', 'SKEJ', 'SKFL', 'SKFR', 'SKGB', 'SKGI', 'SKGO', 'SKGP', 'SKGY', 'SKGZ', 'SKHA', 'SKHC', 'SKHZ',
>>            'SKIB', 'SKIG', 'SKIP', 'SKJC', 'SKLA', 'SKLC', 'SKLG', 'SKLP', 'SKLT', 'SKMA', 'SKMD', 'SKME', 'SKMF', 'SKMN',
>>            'SKMO', 'SKMU', 'SKMZ', 'SKNA', 'SKNQ', 'SKNV', 'SKOC', 'SKOE', 'SKOT', 'SKPA', 'SKPC', 'SKPD', 'SKPE', 'SKPG',
>>            'SKPI', 'SKPN', 'SKPP', 'SKPQ', 'SKPR', 'SKPS', 'SKPZ', 'SKQU', 'SKRG', 'SKSA', 'SKSF', 'SKSG', 'SKSJ', 'SKSO',
>>            'SKSV', 'SKTD', 'SKTI', 'SKTJ', 'SKTM', 'SKTQ', 'SKTU', 'SKUA', 'SKUC', 'SKUI', 'SKUL', 'SKUR', 'SKVG', 'SKVN',
>>            'SKVV', 'SKYP', 'SQUJ', 'SKED', 'SKEC']
>>
>>CENTER = ['SKEC', 'SKED']
>>```
>> [!CAUTION] See how on `CENTER_MAPPING` *Centers* are also inside the dictionary.



Made with love by [657678](http://ivao.aero/Member.aspx?Id=657678)

