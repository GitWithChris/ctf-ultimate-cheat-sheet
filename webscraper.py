""" 
Importieren des BeautifulSoup packages 
Importieren des request packages
"""
from bs4 import BeautifulSoup
import requests



# Bezeichnung der Start-CTF als Variable
ctf_name = 'empire-breakout-vulnhub'



"""
Url welche herangezogen wird als Variable speichern
f'' kennzeichnet den String als einen formatierten String, d.h. im String können nachträglich Änderungen vorgenommen werden
"""
# url = f'https://resources.infosecinstitute.com/topic/{ctf_name}-ctf-walkthrough-part-1/'
#main_url = f'https://resources.infosecinstitute.com/topic/{ctf_name}-ctf-walkthrough/'
main_url = f'https://resources.infosecinstitute.com/topic/empire-breakout-vulnhub-ctf-walkthrough/'



# HTML der Webseite abrufen lassen
main_page = requests.get(main_url)            # sendet einen html request an die angegebene url
html_content_main = main_page.text            # gibt den Inhalt der Antwort als text aus und weist diese der Variablen html_content zu



# Soup Objekt anlegen: Beatiful Soup greift auf Content der Variablen page zu. Html Parser teilt die Inhalte in Html Abschnitte auf
soup = BeautifulSoup(html_content_main, "html.parser")



# Verlinkungen auf der Main-Seite finden
links = soup.select("#in-this-series a")



# Liste für gesammelten Inhalte anlegen
content_list = []




# Schleife über die gefundenen Links
for link in links:                          # jeder link steht für eine Challenge
    challenge_name = link.text.strip()      # aktueller Link wird extrahiert, um den Challenge Namen zu bekommen
    challenge_url = link["href"]            # aktueller Link wird extrahiert, um die Challenge URL zu bekommen
    
    # Anforderung der Challenge-Seite
    challenge_response = requests.get(challenge_url)                                # HTML-Inhalte der aktuellen Webseite abrufen und speichern
    challenge_soup = BeautifulSoup(challenge_response.content, "html.parser")       # HTML-Inhalte parsen und soup erstellen
    
    # Extrahieren des HTML-Inhalts der Challenge-Seite und abspeichern dieser in tags
    # tags = challenge_soup.find_all(string=lambda text: text and "<< " in text and " >>" in text)
    tags = challenge_soup.find_all(string=lambda text: bool(text and "<< " in text and " >>" in text))
    content_list.extend([tag.strip("<< >>").strip() for tag in tags])



with open("all_extracted_contents.txt", "a") as file:
    # file.write(challenge_name + "\n\n")
    file.write("\n".join(content_list) + "\n\n\n")


    


"""
# Speichern des Inhalts in einer Datei
with open("all_extracted_contents.txt", "a") as file:
    file.write(challenge_name + "\n\n")
    file.write("\n".join(content_list) + "\n\n\n")
"""




"""
Tags mit gewünschtem Muster finden
find_all --> finden aller Tags, die eine bestimmte Bedingung erfüllen
text=lambda --> Text ist der Eingabewert der Lambda Funktion. Lambda Funktion nimmt den Text eines Tags als Eingabe-Wert und überprüft ihn auf bestimmte Eigenschaften (siehe nachfolgend)
text: text --> der Eingabeparameter wird direkt zurückgegeben
"<< " --> der Text muss mit dieser Zeichenfolge beginnen
" >>" --> der Text muss mit dieser Zeichenfolge enden

# tags = soup.find_all(text=lambda text: text and "<< " in text and " >>" in text)
tags = soup.find_all(string=lambda text: bool(text and "<< " in text and " >>" in text))

# Inhalte extrahieren und zur Liste anhängen 
for tag in tags:                                # iteriern durch die Liste der gefundenen Tags
    content = tag.strip("<< >>").strip()        # Inhalt jedes Tags wird genommen und die Zeichen << und >> werden entfernt. Der bereinigte Inhalt wird in die Variable gespeichert
    content_list.append(content)



# Inhalte in Tabelle speichern und ausgeben
table = "\n".join(content_list)                 # kombiniert die Inhalte der Liste zu einem einzelnen String. Jeder Inhalt ist durch einen Zeilenumbruch "\n" getrennt
print(table)


with open("extracted_contents.txt", "w") as file:
    for content in content_list:
        file.write(content + "\n")
"""



