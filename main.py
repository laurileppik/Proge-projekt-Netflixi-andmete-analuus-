import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg

df = pd.read_csv('ViewingActivity.csv')

#df.head(1) väljastab kogu esimese rea info
#print(df.head(1))
#df.dtypes väljastab andmeklassid
#print(df.dtypes)

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

#Küsin filminime ja filtreerin välja filmid, mida on vaadetud alla minuti
filminimi=input("Sisesta film/sari mille kohta tahad infot saada! ")
film=df[df['Title'].str.contains(filminimi, regex=False)]
film = film[(film['Duration'] > '0 days 00:01:00')]

#Sorteerin vaatamise nädalapäevadeks ja tundideks
film['weekday'] = film['Start Time'].dt.weekday
film['hour'] = film['Start Time'].dt.hour

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

print(f"Tere {nimi()}!")

if mitu_osa(film)>3:
    print(f"Oled vaadanud seda sarja {tunde_vaatamisele(film)}.")
    print(f"Oled vaadanud {mitu_osa(film)} osa sarja {filminimi}.")
    print(f"Keskmiselt vaatasid seda sarja järjest {keskmiselt_vaatasid(film)}")
else:
    print(f"Oled vaadanud seda filmi {tunde_vaatamisele(film)}.")
    print(f"Oled vaadanud {mitu_osa(film)} osa filmi{filminimi}.")
    print(f"Keskmiselt vaatasid seda filmi järjest {keskmiselt_vaatasid(film)}")

if PCjaTelo()[0]>PCjaTelo()[1]:
    print("Kasutad Netflixi vaatamiseks rohkem arvutit kui telefoni.")
elif PCjaTelo()[0]<PCjaTelo()[1]:
    print("Kasutad Netflixi vaatamiseks rohkem telefoni kui arvutit.")
else:
    print("Kasutad Netflixi vaatamiseks sama palju nii telefoni kui ka arvutit.")
millal_vaadatud(film)
kellal_vaadatud(film)