import sys
import streamlit as st
from pygenomeviz import GenomeViz, track
from operator import itemgetter
import pandas as pd


def parse_gene_data(file):
    genome_list = []
    file.seek(0)  # Revenir au début du fichier si nécessaire
    next(file)  # Pour sauter l'en-tête, si présent
    for line in file:
        parts = line.decode('utf-8').strip().split(';')  # Assurez-vous de décoder si nécessaire
        genome_name = parts[0]
        size = int(parts[1])
        start = max(0, int(parts[2]))
        end = min(size, int(parts[3]))
        strand = int(parts[4])
        color = parts[5]
        genome_list.append(
            {"name": genome_name, "size": size, "start": start, "end": end, "strand": strand, "color": color})

    sorted_genome_list = sorted(genome_list, key=itemgetter('name'))

    return sorted_genome_list



def generate_visualization(input_file):
    genome_list = parse_gene_data(input_file)
    unique_genome = set()
    gv = GenomeViz(tick_style="axis")
    genome_tracks = {}

    for genome in genome_list:
        name, size, start, end, strand, color = genome["name"], genome["size"], genome["start"], genome["end"], genome[
            "strand"], genome["color"]
        unique_genome.add(name)

        if name not in genome_tracks:
            genome_tracks[name] = gv.add_feature_track(name, size)

        track = genome_tracks[name]
        track.add_feature(start, end, strand, label=name, linewidth=1, labelrotation=0, labelvpos="top",
                          labelhpos="center", labelha="center", facecolor=color, edgecolor=color)

    list_unique_genome = list(sorted(unique_genome))
    for i in range(len(list_unique_genome)):
        genomes = [genome for genome in genome_list if genome["name"] == list_unique_genome[i]]
        index = i + 1
        while index < len(genome_list) - 1 and genome_list[index]["name"] == list_unique_genome[i]:
            index += 1
        next_genoms = [genome for genome in genome_list if genome["name"] == genome_list[index]["name"]]

        for z in range(len(genomes)):
            current_genome = genomes[z]
            for y in range(len(next_genoms)):
                next_genome = next_genoms[y]
                if current_genome["name"] != next_genome["name"]:
                    gv.add_link((current_genome["name"], current_genome["start"], current_genome["end"]),
                                (next_genome["name"], next_genome["start"], next_genome["end"]))
    gv.savefig("genome_viz.png")
    return "genome_viz.png"


# Cette fonction vérifie si le script est exécuté via la ligne de commande ou via Streamlit
def main():
    # Mode exécution Streamlit
    if 'streamlit' in sys.modules:
        st.title("Visualisation de Génomes")

        # Upload du fichier
        uploaded_file = st.file_uploader("Chargez un fichier CSV ou TSV", type=["csv", "tsv"])
        if uploaded_file is not None:
            st.write("filename:", uploaded_file.name)

            file_extension = uploaded_file.name.split('.')[-1]
            if file_extension == '.csv':
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file, sep='\t')


            # Génération de la visualisation
            image_path = generate_visualization(uploaded_file)

            # Affichage de l'image
            st.image(image_path)

    # Mode exécution ligne de commande
    else:
        if len(sys.argv) != 2:
            print("Utilisation: python image_Genom.py <fichier.tsv/csv>")
            sys.exit(1)

        input_file = sys.argv[1]
        generate_visualization(input_file)


if __name__ == "__main__":
    main()
