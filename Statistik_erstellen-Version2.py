import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher
import re

# Funktion zum Bereinigen von Linux-Kommandos
def clean_command(command):
    # Entfernen von Leerzeichen am Anfang und Ende des Kommandos
    command = command.strip()
    return command

# Funktion zum Überprüfen, ob eine Zeile einem Linux-Befehl entspricht
def is_linux_command(line):
    # Hier verwenden wir ein einfaches Muster für die Linux-Befehle.
    # Sie können dieses Muster an Ihre spezifischen Anforderungen anpassen.
    pattern = r'^[a-zA-Z]+\s.*$'  # Linux-Befehle beginnen mit Buchstaben gefolgt von Leerzeichen
    return re.match(pattern, line) is not None

# Funktion zum Berechnen der Ähnlichkeit zwischen zwei Zeilen
def calculate_similarity(line1, line2):
    return SequenceMatcher(None, line1, line2).ratio()

# Funktion zum Gruppieren ähnlicher Zeilen und Benennen der Gruppen
def group_similar_lines(lines):
    groups = []
    group_names = []

    for line in lines:
        if line.strip() == '' or line.strip() == 'echo $$' or line.startswith('Challenge') or not is_linux_command(line):
            continue
        cleaned_line = clean_command(line)
        added = False
        for i, group in enumerate(groups):
            similarity = calculate_similarity(cleaned_line, clean_command(group[0]))
            if similarity >= 0.4:
                group.append(line)
                added = True
                break
        if not added:
            groups.append([line])
            group_names.append(line)

    return groups, group_names

# Funktion zum Einlesen der Textdatei, Ausführen des Gruppierungsprozesses und Erstellen des Balkendiagramms
def process_text_file(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    groups, group_names = group_similar_lines(lines)

    # Ausgabe der Gruppen und Befehle in der Konsole
    for i, group in enumerate(groups):
        group_name = group_names[i]
        command_list = '\n'.join(group)
        print(f'{group_name}:')
        print(command_list)
        print()

    # Erstellen des Balkendiagramms
    create_bar_chart(groups, group_names)

# Funktion zum Erstellen des Balkendiagramms
def create_bar_chart(groups, group_names):
    group_sizes = [len(group) for group in groups]

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.8
    bar_positions = np.arange(len(group_sizes))

    ax.bar(bar_positions, group_sizes, width=bar_width)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([])  # Keine Labels auf der X-Achse
    ax.set_xlabel('Group')
    ax.set_ylabel('Count')
    ax.set_title('Similarity Groups')

    # Gruppennummern unterhalb der X-Achse anzeigen
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([f'Group {i+1}' for i in range(len(bar_positions))], rotation=45, ha='right')

    # Erstellen der Legende
    legend_labels = [f"Group {i+1}: {name}" for i, name in enumerate(group_names)]
    legend_text = '\n'.join(legend_labels)

    fig_legend, ax_legend = plt.subplots()
    ax_legend.axis('off')
    ax_legend.text(0, 0, legend_text, fontsize=8)

    plt.tight_layout()
    plt.show()

# Beispielaufruf für die Textdatei 'Kommandos.txt'
process_text_file('Kommandos.txt')
