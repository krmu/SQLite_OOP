import PySimpleGUI as sg
from bazes_modelis import Apstrade
sg.theme("Material2")
# Izsaucam datubāzes operācijas. Atrodas failā bazes_modelis.py
dati = Apstrade()
layout = [[sg.Button("Jauns skolēns", key="jauns_skolens"),sg.Button("Jauns priekšmets", key="jauns_prieksmets"),sg.Button("Viss skolēnu saraksts", key="visi_skoleni")],
          [sg.Button("Visi mācību priekšmeti", key="visi_macibu_prieksmeti"),sg.Button("Mainīt mācību priekšmeta nosaukumu", key="labot_macibu_prieksmetu")],
          [sg.Button("Skolēna vidējie vērtējumi", key="skolena_videjie_vertejumi"),sg.Button("Visu skolēnu vidējie vērtējumi", key="visu_skolenu_videjie_vertejumi")],
          [sg.Button("Vidējais vērtējums mācību priekšmetos", key="videjaisnovisa")],[sg.Button("Vērtējumu ievade", key="vertejumu_ievade")]]
galvenais_logs = sg.Window("Skolēnu datubāze", layout)
def izveles_lodzins(title, text, values):
    window = sg.Window(title,
        [[sg.Text(text)],
        [sg.DropDown(values, key='-DROP-')],
        [sg.OK(), sg.Cancel()]
    ])
    event, values = window.read()
    window.close()
    del window
    return None if event != 'OK' else values['-DROP-']

while True:
    # darbibas_veids -> poga, kura nospiesta vai vispārējais loga stāvoklis.
     
    darbibas_veids, values = galvenais_logs.read()
    if darbibas_veids == "Exit" or darbibas_veids == sg.WIN_CLOSED:
        break
    else:
        title = "Informācija"
        if(darbibas_veids == "videjaisnovisa"):
            dati_atbilde = dati.videjais()
            teksts = ""
            for d in dati_atbilde:
                teksts  =  teksts + "Priekšmets: "+ d['nosaukums'] + ", vērtējums: "+str(d['videjais'])+"\n"
            layout = [[sg.Text(teksts)]]
            title = "Visu mācību priekšmetu vidējie vērtējumi"
        elif darbibas_veids == "visi_macibu_prieksmeti":
            dati_atbilde = dati.visi_macibu_prieksmeti()
            teksts = ""
            for d in dati_atbilde:
                teksts  =  teksts + f"Priekšmets: {d['nosaukums']}, ID: {d['id']} \n"
            layout = [[sg.Text(teksts)]]
            title = "Visi mācību priekšmeti datubāzē"
        elif darbibas_veids == "skolena_videjie_vertejumi":
            skolens = sg.popup_get_text('Ievadiet skolēna uzvārdu: ', title="Skolēna uzvārds") 
            if skolens is None: continue
            dati_atbilde = dati.skolena_videjais(skolens)
            if(len(dati_atbilde) > 0):
                title = f"Skolēns: {dati_atbilde[0]['vards']} {dati_atbilde[0]['uzvards']} \n"
                teksts = ""
                for d in dati_atbilde:
                    teksts  =  teksts + f"Priekšmets: {d['nosaukums']}, Vērtējums: {d['atzime']} \n"
            else:
                teksts = "Datu nav."
            layout = [[sg.Text(teksts)]]
        elif darbibas_veids == "jauns_skolens":
            vards = sg.popup_get_text('Ievadiet skolēna vārdu: ', title="Skolēna vārds") 
            uzvards = sg.popup_get_text('Ievadiet skolēna uzvārdu: ', title="Skolēna uzvārds")
            studenta_kods = sg.popup_get_text('Ievadiet skolēna kodu: ', title="Skolēna kods")
            dati.jauns_skolens(vards,uzvards,studenta_kods)
            layout = [[sg.Text("Skolēns pievienots!")]]
        elif darbibas_veids == "jauns_prieksmets":
            nosaukums = sg.popup_get_text('Ievadiet priekšmeta nosaukumu: ', title="Mācību priekšmeta nosaukums")
            if nosaukums is None: continue
            dati.jauns_prieksmets(nosaukums)
            layout = [[sg.Text("Priekšmets tika pievienots!")]]
        elif darbibas_veids == "visu_skolenu_videjie_vertejumi":
            cik_skoleni = sg.popup_get_text('Cik skolēnus atrādīt: ', title="Skolēnu skaits")
            if cik_skoleni is None: continue
            dati_atbilde = dati.visu_skolenu_videjie(cik_skoleni)
            teksts = ""
            for d in dati_atbilde:
                teksts  =  teksts + f"Skolēns: {d['vards']} {d['uzvards']}, priekšmets: {d['nosaukums']}, vērtējums: {d['videjais']} \n"
            layout = [[sg.Column([[sg.Text(teksts)]], size=(800, 300), scrollable=True)]]
        elif darbibas_veids == "visi_skoleni":
            dati_atbilde = dati.viss_skolenu_saraksts()
            teksts = ""
            for d in dati_atbilde:
                teksts  =  teksts + f"Vārds: {d['vards']}, uzvārds: {d['uzvards']},kods: {d['studenta_kods']}, identifikators: {d['uuid']} \n"
            layout = [[sg.Column([[sg.Text(teksts)]], size=(800, 300), scrollable=True)]]
        elif darbibas_veids == "labot_macibu_prieksmetu":
            ko_labot = sg.popup_get_text('Labojamā mācību priekšmeta nosaukums: ', title="Mācību priekšmeta nosaukums")
            if ko_labot is None: continue
            dati_atbilde  = dati.ir_tads_prieksmets(ko_labot)
            if(dati_atbilde is not None):
                jaunais_nosaukums = sg.popup_get_text('Jaunais nosaukums: ', title=dati_atbilde['nosaukums'])
                if jaunais_nosaukums is None: continue
                dati.labot_macibu_prieksmeta_nosaukumu(jaunais_nosaukums,dati_atbilde['id'])
                layout = [[sg.Text("Mācību priekšmeta nosaukums mainīts!")]]
            else:
                layout = [[sg.Text("Mācību priekšmets nav atrasts vai atrasto priekšmetu skaits ir lielāks par 1.")]]
        elif darbibas_veids == "vertejumu_ievade":
            #macibu_prieksmets = sg.Listbox([1,2,3,4], size=(20,4), enable_events=False, key='_LIST_')
            macibu_prieksmets = izveles_lodzins('Mācību priekšmeta nosaukums', 'Atzīmju ievades mācību priekšmeta nosaukums:', [x['nosaukums'] for x in dati.visi_macibu_prieksmeti()])
            dati_atbilde = dati.atzimes_macibu_prieksmeta(macibu_prieksmets)
            if dati_atbilde is not None:
                title = dati_atbilde[0]['prieksmeta_nosaukums']  + " - vērtējumu ievade"           
                layout = [[sg.Text("Lai dzēstu vērtējumu, jāievada burts d ")]]
                # Zīmē tabulu ar skolēniem un blakus ievades lauku vērtējumam
                summa = 0
                cik_atzimes = 0
                for d in dati_atbilde:
                    #layout.append([sg.Text(f"{d['vards']} {d['uzvards']}", size=60),sg.Input(d['atzime'],key=d['atzimesID'], size=10)])
                    layout.append([sg.Text(f"{d['vards']} {d['uzvards']}", size=60),sg.Combo(["d",1,2,3,4,5,6,7,8,9,10],default_value=d['atzime'],key=d['atzimesID'], size=10)])
                    if d['atzime'] != "" and d['atzime'] is not None:
                        summa += int(d['atzime'])
                        cik_atzimes += 1
                layout.append([sg.Text("Klases vidējais vērtējums:", size=60),sg.Text(round(summa/cik_atzimes,2))])
                layout.append([sg.Button('Saglabāt vērtības datubāzē', key="SaglabatAtzimesDB")])
            else:    
                layout = [[sg.Text("Neatrada mācību priekšmetu")]]
        else:   
            layout = [[sg.Text(darbibas_veids, key="new")]]
        # logā iekšā ir iepriekš jau uzģenerēts saturs.
        papildus_logs = sg.Window(title, layout, modal=True) 
        while True:
            # Darbojas kamēr iziet.
            event, values = papildus_logs.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "SaglabatAtzimesDB":
                for atzimesid, vertejums in values.items():
                    if vertejums == "d":
                        dati.dzest_atzimi(atzimesid)
                    else:
                        atbilde = dati.mainit_atzimi(atzimesid,vertejums)
                        if atbilde is not None:
                            sg.PopupError(atbilde)
                papildus_logs.close()
                sg.PopupAutoClose("Atzīmju atjaunināšana veiksmīga!")                
        papildus_logs.close()
galvenais_logs.close()