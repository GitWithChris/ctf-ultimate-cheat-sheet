import matplotlib.pyplot as plt
import numpy as np
from difflib import SequenceMatcher

# Funktion zum Berechnen der Ähnlichkeit zwischen zwei Zeilen
def calculate_similarity(line1, line2):
    return SequenceMatcher(None, line1, line2).ratio()

# Funktion zum Gruppieren ähnlicher Zeilen und Benennen der Gruppen
def group_similar_lines(lines):
    groups = []
    group_names = []

    for line in lines:
        if line.strip() == '' or line.strip() == 'echo $$' or line.startswith('Challenge'):
            continue
        added = False
        for i, group in enumerate(groups):
            similarity = calculate_similarity(line, group[0])
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
    group_labels = [f"Group {i+1}" for i in range(len(groups))]
    group_sizes = [len(group) for group in groups]

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.8
    bar_positions = np.arange(len(group_labels))

    ax.bar(bar_positions, group_sizes, width=bar_width)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(group_labels, rotation=45, ha='right', fontsize=6)
    ax.set_xlabel('Group')
    ax.set_ylabel('Count')
    ax.set_title('Similarity Groups')

    for i, size in enumerate(group_sizes):
        ax.text(i, size + 0.5, "", ha='center', fontsize=6)

    ax.legend(group_names, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

    plt.tight_layout()

    # Erstellen der Legende
    legend_labels = [f"Group {i+1}: {name}" for i, name in enumerate(group_names)]
    legend_text = '\n'.join(legend_labels)

    # Einbetten des Diagramms in ein Scrollfenster mit der Legende unterhalb des Diagramms
    fig, ax_scrolling = plt.subplots(figsize=(12, 6))
    ax_scrolling.axis('off')
    ax_scrolling.text(0, 0.5, legend_text, fontsize=8, verticalalignment='top')

    plt.show()

# Beispielaufruf für die Textdatei 'Kommandos.txt'
process_text_file('Kommandos.txt')
