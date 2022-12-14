import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as ui
import math
from collections import Counter

#Funktsioon tagastab kui mitu tundi on filmi/sarja vaadatud
def tunde_vaatamisele(film):
    tunnid_vaatamisele=film['Duration'].sum()
    tunnid_vaatamisele=str(tunnid_vaatamisele)
    tunnid_vaatamisele=tunnid_vaatamisele.replace("days"," päeva")
    tunnid_vaatamisele=tunnid_vaatamisele.replace(":"," tundi ",1)
    tunnid_vaatamisele=tunnid_vaatamisele.replace(":"," minutit ",1)
    tunnid_vaatamisele=tunnid_vaatamisele + " sekundit"
    if tunnid_vaatamisele[:1]=="0":
        return(tunnid_vaatamisele[9:])
    else:
        return(tunnid_vaatamisele)

#Funktsioon tagastab kui kaua vaatasid filmi järjest
def keskmiselt_vaatasid(film):
    tunnid_vaatamisele=film['Duration'].sum()
    filme_kokku=film['Duration'].count()
    keskmine=tunnid_vaatamisele/filme_kokku
    keskmine=str(keskmine)
    keskmine=keskmine.replace(" days ",":")
    keskmine=keskmine.split(":")
    if keskmine[0]=="0" and keskmine[1]=="00":
        keskmine2=round(float(keskmine[3]))
        keskmine=str(keskmine[2]) + " minutit " + str(keskmine2) + " sekundit."
        return keskmine
    return keskmine

#Funktsioon tagastab mitu osa on filmi vaadatud
def mitu_osa(film):
    shape=film.shape
    tunde=shape[0]
    return tunde

#Funktsioon tagastab mitu korda on vaadatud filme/sarju [arvutist,telefonist]
def PCjaTelo():
    list=[]
    PC= df['Device Type'].str.contains('PC|MAC|Windows').sum()
    list.append(PC)
    Telo= df['Device Type'].str.contains('Phone|Android|Mobile').sum()
    list.append(Telo)
    TV= df['Device Type'].str.contains('TV').sum()
    list.append(TV)
    return list

#Funktsioon tagastab programmi kasutaja nime.
def nimi():
    nimi=df["Profile Name"]
    return(nimi[0])

#Funktsioon mis tagastab kõige rohkem tunde vaadatud sarja
def enim_vaadatud():
    list1 = df["Duration"].values.tolist()
    list2 = df["Title"].values.tolist()
    õige_nimi=[]
    for i in list2:
        i=i.replace("_hook_",":")
        i=i.split(":")
        i=i[:1]
        õige_nimi.append(i)
    
    sõn={}

    if len(list1) == len(õige_nimi):
        for i in range(len(õige_nimi)):
            if õige_nimi[i][0] not in sõn:
                sõn[õige_nimi[i][0]] = 0

            sõn[õige_nimi[i][0]] += list1[i]

    siiani_max=0
    for i in sõn.items():
        if i[1]>siiani_max:
            siiani_max=i[1]
            voitja=i[0]
        else:
            continue
    return voitja

#Funktsioon mis tagastab kogu Netflixis veedetud aja.
def kogu_aeg():
    tunnid_vaatamisele = str(df["Duration"].sum())
    print(tunnid_vaatamisele)
    tunnid_vaatamisele=tunnid_vaatamisele.replace(" days "," päeva ")
    tunnid_vaatamisele=tunnid_vaatamisele.replace(":"," tundi ",1)
    tunnid_vaatamisele=tunnid_vaatamisele.replace(":"," minutit ")
    tunnid_vaatamisele=tunnid_vaatamisele + " sekundit"

    if tunnid_vaatamisele[0]==0:
        tunnid_vaatamisele=tunnid_vaatamisele.replace("0 päeva ","") 
    else:
        return tunnid_vaatamisele

#Funktsioon mis teeb graafiku vaatamise jaotusest üle päevade
def millal_vaadatud(film):
    film['weekday'] = pd.Categorical(film['weekday'], categories=[0,1,2,3,4,5,6], ordered=True)
    film_päeviti = film["weekday"].value_counts()
    film_päeviti = film_päeviti.sort_index()
    plt.rcParams.update({'font.size': 20})
    film_päeviti.plot(kind='bar', figsize=(20,10), title="Vaatamise jaotus üle päevade")
    plt.xlabel("Päevad esmaspäevast pühapäevani")
    plt.ylabel("Osade arv")
    plt.show()

#Funktsioon mis teeb graafiku vaatamise jaotusest üle kellaaja
def kellal_vaadatud(film):
    film['hour'] = pd.Categorical(film['hour'], categories=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], ordered=True)
    film_tunniti = film['hour'].value_counts()
    film_tunniti = film_tunniti.sort_index()
    film_tunniti.plot(kind='bar', figsize=(20,10), title="Vaatamise jaotus üle tundide")
    plt.xlabel("Kellaaeg 00-st 23-ni")
    plt.ylabel("Osade arv")
    plt.show()

#Funktsioon, mis tagastab kõik filmid hulgana
#HETKEL VEEL PROBLEEM, ET TAGASTAB NONE ILMA PÕHJUSETA KUI KINNI PANNA
def kõik_filmid():
    #Eemaldab kõik alla minutised vaatamised
    pikkus = pd.to_timedelta(df['Duration'])
    pikkus = pikkus.apply(lambda x: x.value)
    uusdf=df[(pikkus) >= 60000000000]

    #Esialgu tekitab listi kõikidest filmidest
    õige_filmid=[]
    filmid = uusdf["Title"].values.tolist()
    for i in filmid:
        i=i.replace("_hook_",":")
        i=i.replace(" - C",":")
        i=i.split(":")
        i=i[:1]
        i=i[0]
        õige_filmid.append(i)
    filmid=set(õige_filmid)
    filmid=list(filmid)
    filmid.sort()

    layout2=[[ui.Text("Kõik filmid")],[ui.Combo(filmid,key='board')],
    [ui.Push(), ui.Exit(button_text="Sulge", button_color="tomato", s=15)] ]
    window2 = ui.Window("Kõik filmid", layout2, use_custom_titlebar=True)
    while True:
        event, values = window2.Read()
        if event in (ui.WINDOW_CLOSED, "Sulge"):
            break
    window2.close()
    
#UI akna layout ja theme
ui.theme("DarkBlue14")
layout = [  [ui.Text("Vali Netflixi andmete fail"), ui.Input(key="-FILE_PATH-"), ui.FileBrowse("Sirvi", file_types=(("CSV failid", "*.csv"),))],
            [ui.Text("Sisesta film/sari mille kohta soovid statistikat:"), ui.Input(key="-FILM-")],
            [ui.Text("Sisesta oma Netflixi kasutajanimi:"), ui.Input(key="-NIMI-")],
            [ui.Button("Kinnita")],
            [ui.Text("Funktsioonid (Kasuta peale kinnitamist):")],
            [ui.Button("Kõik vaadatud Netflixi filmid/sarjad")],[ui.Button("Kui kaua vaatasid filmi/sarja kokku")],[ui.Button("Millist seadet kasutasid vaatamiseks rohkem")], [ui.Button("Millal vaatasid filmi/sarja nädala lõikes")], [ui.Button("Millal vaatasid filmi/sarja tunni lõikes")],
            [ui.Button("Missugust sarja oled kõige rohkem vaadanud")], [ui.Button("Kui palju oled sa kokku Netflixi vaadanud")], [ui.Push(), ui.Exit(button_text="Sulge", button_color="tomato", s=15)]   ]

#UI aken
window = ui.Window("Netflixi vaatamise statistika", layout, use_custom_titlebar=True)

while True: # Võibolla ei peaks while loopi kasutama
    event, values = window.Read()
    if event == "Kinnita":
        failiasukoht=values["-FILE_PATH-"]
        filminimi=values["-FILM-"]
        sinunimi=values["-NIMI-"]
        #Küsin filminime 
        df = pd.read_csv(failiasukoht)

        #Filtreerib välja read, mis ei ole seotud antud nimedega
        values=[sinunimi]
        df=df.query("`Profile Name` in @values")
        #Eemaldan trailerid ja hookid
        values2=["HOOK","TRAILER"]
        df=df.query("`Supplemental Video Type` not in @values2")
        #Selle reaga teen starttime pandale loetavaks
        df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
        #Nende 3 reaga muudan UTC EETks
        df = df.set_index('Start Time')
        df.index = df.index.tz_convert('EET')
        df = df.reset_index()
        #Eemaldan veerud mida ei kavatse kasutada
        df = df.drop(['Attributes', 'Latest Bookmark', 'Supplemental Video Type', 'Country'], axis=1)
        #Muudan kestvuse pandale arusaadavaks ja filtreerin välja filmid, mida on vaadetud alla minuti
        df['Duration'] = pd.to_timedelta(df['Duration'])
        film=df[df['Title'].str.contains(filminimi, regex=False)]
        film = film[(film['Duration'] > '0 days 00:01:00')]
        #Sorteerin vaatamise nädalapäevadeks ja tundideks
        film['weekday'] = film['Start Time'].dt.weekday
        film['hour'] = film['Start Time'].dt.hour

        if failiasukoht=="":
            ui.popup_error("Palun vali fail", keep_on_top=True) #errorid ei, tööta praegu see crashib lihtsalt
        elif filminimi=="":
            ui.popup_error("Palun sisesta filmi/sarja nimi", keep_on_top=True) 
        else:
            ui.popup(f"Tere {nimi()}!\nFail on valitud ja saate nüüd kasutada funktsioone!", keep_on_top=True, title="Kinnitus")
    
    elif event == "Kõik vaadatud Netflixi filmid/sarjad":
        ui.popup(f"{kõik_filmid()}", title="Kõik vaadatud Netflixi filmid/sarjad", keep_on_top=True)
    
    elif event == "Kui kaua vaatasid filmi/sarja kokku":
        if mitu_osa(film)>3:
            ui.popup(f"Kokku vaatasid sarja {filminimi} {mitu_osa(film)} osa.\nVaatamisele kulus {tunde_vaatamisele(film)}\nKeskmiselt vaatasid järjest {keskmiselt_vaatasid(film)}", title="Kui kaua vaatasid sarja kokku", keep_on_top=True)
        else:
            ui.popup(f"Kokku vaatasid filmi {filminimi} {mitu_osa(film)} osa.\nVaatamisele kulus {tunde_vaatamisele(film)}\nKeskmiselt vaatasid järjest {keskmiselt_vaatasid(film)}", title="Kui kaua vaatasid filmi kokku", keep_on_top=True)

    elif event == "Millist seadet kasutasid vaatamiseks rohkem":
        if PCjaTelo()[2]>PCjaTelo()[0] and PCjaTelo()[2]>PCjaTelo()[1]:
            ui.popup(f"Kasutasid Netflixi vaatamiseks kõige rohkem telekat.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
        elif PCjaTelo()[1]<PCjaTelo()[0]:
            ui.popup(f"Kasutasid Netflixi vaatamiseks kõige rohkem arvutit.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
        elif PCjaTelo()[0]<PCjaTelo()[1]:
            ui.popup(f"Kasutasid Netflixi vaatamiseks kõige rohkem telefoni.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
        else:
            ui.popup(f"Kasutasid Netflixi vaatamiseks sama palju nii telefoni, telekat kui ka arvutit.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
    
    elif event == "Kui palju oled sa kokku Netflixi vaadanud":
        ui.popup(f"Oled kokku vaadanud Netflixi {kogu_aeg()}.", keep_on_top=True, title="Kui palju oled sa kokku Netflixi vaadanud")

    elif event == "Missugust sarja oled kõige rohkem vaadanud":
        ui.popup(f"Oled kõige rohkem vaadanud sarja {enim_vaadatud()}.", keep_on_top=True, title="Millist sarja oled kõige rohkem vaadanud")

    elif event == "Millal vaatasid filmi/sarja nädala lõikes":
        millal_vaadatud(film)

    elif event == "Millal vaatasid filmi/sarja tunni lõikes":
        kellal_vaadatud(film)

    elif event in (ui.WINDOW_CLOSED, "Sulge"):
        break

#Akna sulgemine
window.close()