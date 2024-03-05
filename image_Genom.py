import sys
import random
from pygenomeviz import GenomeViz, track
from operator import itemgetter


def parse_gene_data(file_path):
    genome_list = []
    with open(file_path, 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split(';')
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


def main(input_file):
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
                    print(current_genome["name"], next_genome["name"])
                    gv.add_link((current_genome["name"], current_genome["start"], current_genome["end"]),
                                (next_genome["name"], next_genome["start"], next_genome["end"]))
    gv.savefig("genome_viz.png")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation: python image_Genom.py <fichier.tsv/csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
