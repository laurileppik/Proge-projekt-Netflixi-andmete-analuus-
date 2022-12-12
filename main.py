import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as ui

#Funktsioon tagastab kui mitu tundi on filmi/sarja vaadatud
def tunde_vaatamisele(film):
    tunnid_vaatamisele=film['Duration'].sum()
    tunnid_vaatamisele=str(tunnid_vaatamisele)
    tunnid_vaatamisele=tunnid_vaatamisele.replace("days"," päeva")
    tunnid_vaatamisele=tunnid_vaatamisele.replace(":"," tundi ",1)
    tunnid_vaatamisele=tunnid_vaatamisele.replace(":"," minutit ",1)
    tunnid_vaatamisele=tunnid_vaatamisele + " sekundit"
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
    PC= df[df['Device Type'].str.contains("PC", regex=False)]
    shape=PC.shape
    PC=shape[0]
    list.append(PC)
    Telo= df[df['Device Type'].str.contains("Phone", regex=False)]
    shape=Telo.shape
    Telo=shape[0]
    list.append(Telo)
    return list

#Funktsioon tagastab programmi kasutaja nime.
def nimi():
    nimi=df["Profile Name"]
    return(nimi[0])

#Funktsioon mis tagastab kõige rohkem tunde vaadatud sarja
#def enim_vaadatud():
#Kood on veel puudu

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

#UI akna layout ja theme
ui.theme("DarkBlue14")
layout = [  [ui.Text("Vali Netflixi andmete fail"), ui.Input(key="-FILE_PATH-"), ui.FileBrowse("Sirvi", file_types=(("CSV failid", "*.csv"),))],
            [ui.Text("Sisesta film/sari mille kohta soovid statistikat:"), ui.Input(key="-FILM-")],
            [ui.Button("Kinnita")],
            [ui.Text("Funktsioonid (Kasuta peale kinnitamist):")],
            [ui.Button("Kui kaua vaatasid filmi/sarja kokku")],[ui.Button("Millist seadet kasutasid vaatamiseks rohkem")], [ui.Button("Millal vaatasid filmi/sarja nädala lõikes")], [ui.Button("Millal vaatasid filmi/sarja tunni lõikes")],
            [ui.Push(), ui.Exit(button_text="Sulge", button_color="tomato", s=15)]   ]

#UI aken
window = ui.Window("Netflixi vaatamise statistika", layout, use_custom_titlebar=True)

while True: # Võibolla ei peaks while loopi kasutama
    event, values = window.Read()
    if event == "Kinnita":
        failiasukoht=values["-FILE_PATH-"]
        filminimi=values["-FILM-"]
        #Küsin filminime ja filtreerin välja filmid, mida on vaadetud alla minuti
        df = pd.read_csv(failiasukoht)
        #Selle reaga teen starttime pandale loetavaks
        df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
        #Nende 3 reaga muudan UTC EETks
        df = df.set_index('Start Time')
        df.index = df.index.tz_convert('EET')
        df = df.reset_index()
        #Eemaldan veerud mida ei kavatse kasutada
        df = df.drop(['Attributes', 'Latest Bookmark', 'Supplemental Video Type', 'Country'], axis=1)
        #Muudan kestvuse pandale arusaadavaks
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
    elif event == "Kui kaua vaatasid filmi/sarja kokku":
        if mitu_osa(film)>3:
            ui.popup(f"Kokku vaatasid sarja {filminimi} {mitu_osa(film)} osa.\nVaatamisele kulus {tunde_vaatamisele(film)}\nKeskmiselt vaatasid järjest {keskmiselt_vaatasid(film)}", title="Kui kaua vaatasid sarja kokku", keep_on_top=True)
        else:
            ui.popup(f"Kokku vaatasid filmi {filminimi} {mitu_osa(film)} osa.\nVaatamisele kulus {tunde_vaatamisele(film)}\nKeskmiselt vaatasid järjest {keskmiselt_vaatasid(film)}", title="Kui kaua vaatasid filmi kokku", keep_on_top=True)
    elif event == "Millist seadet kasutasid vaatamiseks rohkem":
        if PCjaTelo()[0]>PCjaTelo()[1]:
            ui.popup(f"Kasutasid Netflixi vaatamiseks rohkem arvutit kui telefoni.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
        elif PCjaTelo()[0]<PCjaTelo()[1]:
            ui.popup(f"Kasutasid Netflixi vaatamiseks rohkem telefoni kui arvutit.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
        else:
            ui.popup(f"Kasutasid Netflixi vaatamiseks sama palju nii telefoni kui ka arvutit.", title="Millist seadet kasutasid vaatamiseks rohkem", keep_on_top=True)
    elif event == "Millal vaatasid filmi/sarja nädala lõikes":
        millal_vaadatud(film)
    elif event == "Millal vaatasid filmi/sarja tunni lõikes":
        kellal_vaadatud(film)
    elif event in (ui.WINDOW_CLOSED, "Sulge"):
        break

#Akna sulgemine
window.close()