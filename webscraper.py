% Importieren des BeautifulSoup packages 
from bs4 import BeautifulSoup


% Importieren des request packages
import requests


% Bezeichnung der CTF als Variable
ctf_name = 'empire-breakout-vulnhub'


% Url welche herangezogen wird als Variable speichern
% f'' kennzeichnet den String als einen formatierten String, d.h. im String können nachträglich Änderungen vorgenommen werden

url = f'https://resources.infosecinstitute.com/topic/{ctf_name}-ctf-walkthrough-part-1/'


% Python automatisch auf die Url zugreifen lassen und Daten in der Variablen abspeichern lassen

page = requests.get(url)


% Soup Objekt anlegen: Beatiful Soup greift auf Content der Variablen page zu. Html Parser teilt die Inhalte in Html Abschnitte auf

soup = BeautifulSoup(page.content, "html.parser")


print(soup)