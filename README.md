# SQLite_OOP
SQLite piemērs rakstīts uz OOP mācību nolūkiem.
# Datņu saturs
### - vizualais_logs.py 
Galvenā datne, kura jāpalaiž. Jāinstalē pysimplegui! <br>
### - bazes_modelis.py
Datne, kura satur operācijas ar datubāzi.<br>
### - datubaze.db 
Datubāze. Lai atvērtu to -> https://sqlitebrowser.org/<br>
# Datubāzes struktūra
### - atzimes
- **uuid** - Unikālais identifikators UUID v4 formātā.
- **prieksmets** - Unikālais identifikators UUID v4 formātā, kurš atbilst
- **priekšmetu** tabulas ID lauka vērtībai
- **atzime** - skolēna vērtējums no 1 līdz 10
- **pievienots** - laikspiedogs UNIX formātā
- **skolens** - Unikālais identifikators UUID v4 formātā, kurš atbilst skolēnu tabulas uuid lauka vērtībai
### - prieksmeti
- **id** - Unikālais identifikators UUID v4 formātā.
- **nosaukums** - mācību priekšmeta nosaukums teksta formātā
### - skoleni
- **uuid** - Unikālais identifikators UUID v4 formātā
- **vards** - Skolēna vārds
- **uzvards** - Skolēna uzvārds
- **studenta_kods** - Skolēna kods

# Media
## Galvenais logs 
![Attēls](/media/main_logs.png)<br>
## Visas vidējās atzīmes pa priekšmetiem 
![Attēls](/media/visi_videjie.png)<br>
## Viss skolēnu saraksts
![Attēls](/media/viss_skolenu_saraksts.png)
## Atzīmju ievade 
![Attēls](/media/atzimju_ievade1.png)<br>
![Attēls](/media/atzimju_ievade2.png)
## Visu skolēnu vidējie vērtējumi
![Attēls](/media/visu_skolenu_videjie.png)