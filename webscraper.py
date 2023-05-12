""" 
Importieren des BeautifulSoup packages 
Importieren des request packages
"""
from bs4 import BeautifulSoup
import requests


# Bezeichnung der CTF als Variable
ctf_name = 'empire-breakout-vulnhub'


"""
Url welche herangezogen wird als Variable speichern
f'' kennzeichnet den String als einen formatierten String, d.h. im String können nachträglich Änderungen vorgenommen werden
"""
# url = f'https://resources.infosecinstitute.com/topic/{ctf_name}-ctf-walkthrough-part-1/'
url = f'https://resources.infosecinstitute.com/topic/{ctf_name}-ctf-walkthrough/'


# HTML der Webseite abrufen lassen
page = requests.get(url)            # sendet einen html request an die angegebene url
html_content = page.text            # gibt den Inhalt der Antwort als text aus und weist diese der Variablen html_content zu


# Soup Objekt anlegen: Beatiful Soup greift auf Content der Variablen page zu. Html Parser teilt die Inhalte in Html Abschnitte auf
soup = BeautifulSoup(html_content, "html.parser")


# Liste für gesammelten Inhalte anlegen
content_list = []


"""
Tags mit gewünschtem Muster finden
find_all --> finden aller Tags, die eine bestimmte Bedingung erfüllen
text=lambda --> Text ist der Eingabewert der Lambda Funktion. Lambda Funktion nimmt den Text eines Tags als Eingabe-Wert und überprüft ihn auf bestimmte Eigenschaften (siehe nachfolgend)
text: text --> der Eingabeparameter wird direkt zurückgegeben
"<< " --> der Text muss mit dieser Zeichenfolge beginnen
" >>" --> der Text muss mit dieser Zeichenfolge enden
"""
# tags = soup.find_all(text=lambda text: text and "<< " in text and " >>" in text)
tags = soup.find_all(string=lambda text: bool(text and "<< " in text and " >>" in text))

# Inhalte extrahieren und zur Liste anhängen 
for tag in tags:                                # iteriern durch die Liste der gefundenen Tags
    content = tag.strip("<< >>").strip()        # Inhalt jedes Tags wird genommen und die Zeichen << und >> werden entfernt. Der bereinigte Inhalt wird in die Variable gespeichert
    content_list.append(content)


"""
# Inhalte in Tabelle speichern und ausgeben
table = "\n".join(content_list)                 # kombiniert die Inhalte der Liste zu einem einzelnen String. Jeder Inhalt ist durch einen Zeilenumbruch "\n" getrennt
print(table)
"""

with open("extracted_contents.txt", "w") as file:
    for content in content_list:
        file.write(content + "\n")

