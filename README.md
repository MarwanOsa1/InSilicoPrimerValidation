# In Silico Validation of SARS-CoV-2 Primers and Probes

This repository provides pipelines for **computational primer/probe validation** and **lineage assignment** of SARS-CoV-2 genomes.  
It is based on the study:  
👉 [A Novel Quadriplex Reverse Transcription PCR Assay for Robust SARS-CoV-2 Diagnosis and Variant Detection: Experimental Optimization for Enhanced Sensitivity and Specificity](https://link.springer.com/article/10.1134/S1061934825700704)

---

## 📌 Features
- Fetch SARS-CoV-2 genome sequences directly from NCBI using accession IDs.
- Validate primers and probes by local pairwise alignment (identity %, binding sites).
- Export results into Excel (one sheet per gene).
- Assign SARS-CoV-2 lineages using [PANGOLIN](https://github.com/cov-lineages/pangolin).
- Merge primer validation results with lineage data into one master file.

---

## 📂 Repository Layout
```
InSilicoPrimerValidation/
│── README.md
│── requirements.txt
│── Covid_Manuscript.py       # Primer/probe validation
│── hh.sh                     # Lineage assignment
│── combine_results.py         # Merge results
│── .gitignore
│
├── accessions/                # Input accession files (.txt)
│   └── example_accessions.txt
│
├── results/                   # Validation outputs (.xlsx)
│   └── .keep
│
└── lineages/                  # Lineage outputs (.csv)
    └── .keep
```

---

## ⚙️ Requirements
### Python libraries
```bash
pip install -r requirements.txt
```

### External tools
- [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK179288/) (requires email)
- [PANGOLIN](https://github.com/cov-lineages/pangolin):
```bash
conda create -n pangolin -c bioconda -c conda-forge pangolin
```

---

## 🚀 Usage

### 1. Primer/Probe Validation
Place accession ID files in `accessions/` (one ID per line).  
Run:
```bash
python Covid_Manuscript.py --email your@email
```  
Results will appear in `results/` as `.xlsx` files.

### 2. Lineage Assignment
Run:
```bash
bash hh.sh
```  
Lineage CSVs will appear in `lineages/`.

### 3. Combine All Results
Merge validation + lineage results:
```bash
python combine_results.py --output final_results.xlsx
```

---

## 📜 Citation
If you use this repo, please cite:
**Mousa, N., Osama, M., Talkhan, H. et al. A Novel Quadriplex Reverse Transcription PCR Assay for Robust SARS-CoV-2 Diagnosis and Variant Detection: Experimental Optimization for Enhanced Sensitivity and Specificity. J Anal Chem 80, 1471–1482 (2025). https://doi.org/10.1134/S1061934825700704****M. Osama Hashem et al., Journal of Analytical Chemistry, 2025**  


---

## 👤 Author
**Marwan Osama Hashem**  
Graduate researcher in Bioinformatics & Biotechnology
