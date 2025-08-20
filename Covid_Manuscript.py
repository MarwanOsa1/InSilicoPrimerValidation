#!/usr/bin/env python3
import os
import argparse
import pandas as pd
from Bio import SeqIO, pairwise2, Entrez
import time

# -------------------------------------------------
# Custom scoring matrix for primers with ambiguous bases
# -------------------------------------------------
custom_matrix = {
    ('A','A'):1, ('C','C'):1, ('G','G'):1, ('T','T'):1,
    ('N','A'):1, ('N','C'):1, ('N','G'):1, ('N','T'):1, ('N','N'):1,
    ('R','A'):0, ('R','G'):0, ('Y','C'):0, ('Y','T'):0,
}
bases = ['A','C','G','T','N','R','Y']
full_custom_matrix = {(b1,b2): custom_matrix.get((b1,b2), custom_matrix.get((b2,b1), -1)) for b1 in bases for b2 in bases}

primer_pairs = [
    ("Spike_Glycoprotein", "GGCTGTTTAATAGGGGCTGAAN", "AATCCATCATTGCCTACACTATG"),
    ("Envelope_Protein", "GAYAGGTACGTTAATAGTTAATAGCG", "CGTGAGTCTTGTAAAACCTTCTTT"),
    ("Nucleocapsid_Protein", "GCCTCTTCTCGTTCCTCATCAC", "TGAGAGCAAAATGTNTGGTAAAG"),
    ("3'_UTR", "GTGTAACATTAGGGAGGACTTGA", "GCTGCCTATATGGAAGAGCC"),
]
primer_ranges = {
    "Spike_Glycoprotein": (22000, 24999),
    "Envelope_Protein": (25000, 26999),
    "Nucleocapsid_Protein": (27000, 29000),
    "3'_UTR": (27000, 29999)
}

def calculate_identity(seq1, seq2, length):
    matches = sum(1 for a,b in zip(seq1, seq2) if (a==b) or (a,b) in full_custom_matrix and full_custom_matrix[(a,b)]>0)
    return (matches/length)*100

def fetch_sequences(accession_ids, email):
    Entrez.email = email
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession_ids, rettype="fasta", retmode="text")
        seqs = list(SeqIO.parse(handle, "fasta"))
        handle.close()
        return seqs
    except Exception as e:
        print(f"Error fetching sequences: {e}")
        return []

def process_file(file_path, out_dir, email):
    with open(file_path) as f:
        accession_ids = f.read().strip().split()
    if not accession_ids:
        print(f"No IDs found in {file_path}")
        return
    genomes = fetch_sequences(accession_ids, email)
    if not genomes:
        return

    out_file = os.path.join(out_dir, os.path.basename(file_path).replace(".txt","_results.xlsx"))
    results = {g: [] for g,_,_ in primer_pairs}
    for gene,fwd,rev in primer_pairs:
        start,end = primer_ranges[gene]
        for genome in genomes:
            seq = str(genome.seq)
            subseq = seq[start:end]
            result = {"Accession": genome.id, "Sample": genome.description}
            for primer,label in [(fwd,"Forward"), (rev,"Reverse")]:
                alignments = pairwise2.align.localds(primer, subseq, full_custom_matrix, -2, -1)
                if alignments:
                    aln1,aln2,score,s,e = alignments[0]
                    result[f"{label}_Identity"] = calculate_identity(aln1,aln2,len(primer))
                    result[f"{label}_Binding"] = f"{start+s}-{start+e}"
                else:
                    result[f"{label}_Identity"] = None
                    result[f"{label}_Binding"] = None
            results[gene].append(result)
    with pd.ExcelWriter(out_file, engine="openpyxl") as writer:
        for gene,data in results.items():
            pd.DataFrame(data).to_excel(writer, sheet_name=gene,index=False)
    print(f"Saved results -> {out_file}")

def main():
    parser = argparse.ArgumentParser(description="In silico primer/probe validation")
    parser.add_argument("--accession_dir", default="./accessions", help="Directory with accession ID .txt files")
    parser.add_argument("--output_dir", default="./results", help="Output directory for Excel results")
    parser.add_argument("--email", required=True, help="NCBI Entrez email")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    for fname in os.listdir(args.accession_dir):
        if fname.endswith(".txt"):
            print(f"Processing {fname}...")
            process_file(os.path.join(args.accession_dir,fname), args.output_dir, args.email)
            time.sleep(1)

if __name__=="__main__":
    main()
