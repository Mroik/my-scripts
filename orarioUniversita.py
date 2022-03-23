#!/bin/python
import requests
import datetime
import sys

date = datetime.datetime.now()
if len(sys.argv) > 1:
    date = date - datetime.timedelta(days=-1)

course_type = "1+Anno+-+Obbligatori"
school_year = "2020"
course = "F1X"

# Più tardi cercherò di capire cosa vogliano dire i vari campi
req = requests.post("https://easystaff.divsi.unimi.it/PortaleStudenti/grid_call_new.php",
        data = [
            ('date', date.strftime("%d-%m-%G")),
            ('view', 'easycourse'),
            ('form-type', 'corso'),
            ('include', 'corso'),
            ('txtcurr', '2 Anno - Unico'),
            ('txtcurr', '2 Anno - Unico'),
            ('anno', '2021'),
            ('corso', 'F1X'),
            ('anno2[]', 'F1X-0|2'),
            ('periodo_didattico', ''),
            ('_lang', 'it'),
            ('_lang', 'it'),
            ('list', '0'),
            ('week_grid_type', '-1'),
            ('ar_codes_', ''),
            ('ar_select_', ''),
            ('col_cells', '0'),
            ('empty_box', '0'),
            ('only_grid', '0'),
            ('highlighted_date', '0'),
            ('all_events', '0'),
            ('all_events', '0'),
            ('faculty_group', '0'),
        ]
)

for x in req.json()["celle"]:
    to_find = date.strftime("%e")
    try:
        found = x["GiornoCompleto"].split(" ")
        if found[1] == "":
            found = found[2]
        else:
            found = found[1]
    except KeyError:
        continue
    if int(found) == int(to_find):
        print("Giorno: {}".format(x["GiornoCompleto"]))
        print("Docente: {}".format(x["docente"]))
        print("Insegnamento: {}".format(x["nome_insegnamento"]))
        print("Orario: {}-{}".format(x["ora_inizio"], x["ora_fine"]))
        print()
