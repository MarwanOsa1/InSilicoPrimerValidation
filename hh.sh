#!/bin/bash
set -e

INPUT_DIR="./accessions"
OUTPUT_DIR="./lineages"
CONDA_ENV="pangolin"
FILE_PATTERN="combined_accession_ids_*.txt"

mkdir -p "$OUTPUT_DIR"

source ~/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

for FILE in $INPUT_DIR/$FILE_PATTERN; do
  [ -f "$FILE" ] || continue
  echo "Processing $FILE"
  while IFS= read -r acc; do
    [ -z "$acc" ] && continue
    seq=$(esearch -db nucleotide -query "$acc" | efetch -format fasta)
    [ -z "$seq" ] && continue
    out_base=$(basename "$FILE" .txt)
    echo "$seq" | pangolin - > "$OUTPUT_DIR/${out_base}_${acc}_pangolin.txt"
    if [ -f "lineage_report.csv" ]; then
      mv lineage_report.csv "$OUTPUT_DIR/${out_base}_${acc}_lineage.csv"
    fi
  done < "$FILE"
done

conda deactivate
