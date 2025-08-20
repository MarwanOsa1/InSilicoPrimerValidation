#!/usr/bin/env python3
import os
import argparse
import pandas as pd

def combine(excel_dir, lineage_dir, output_file):
    all_frames = []
    for f in os.listdir(excel_dir):
        if f.endswith(".xlsx"):
            excel_path = os.path.join(excel_dir,f)
            xls = pd.ExcelFile(excel_path)
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls,sheet_name=sheet)
                df["Gene"] = sheet
                df["Source_File"] = f
                all_frames.append(df)
    combined = pd.concat(all_frames,ignore_index=True)

    lineage_frames = []
    for f in os.listdir(lineage_dir):
        if f.endswith("_lineage.csv"):
            lineage_frames.append(pd.read_csv(os.path.join(lineage_dir,f)))
    if lineage_frames:
        lineage = pd.concat(lineage_frames,ignore_index=True)
        final = combined.merge(lineage, how="left", left_on="Accession", right_on="taxon")
    else:
        final = combined
    final.to_excel(output_file,index=False)
    print(f"Final combined file saved -> {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Combine primer validation and lineage results")
    parser.add_argument("--excel_dir", default="./results", help="Directory with Excel results")
    parser.add_argument("--lineage_dir", default="./lineages", help="Directory with lineage CSVs")
    parser.add_argument("--output", default="./final_combined.xlsx", help="Output Excel file")
    args = parser.parse_args()
    combine(args.excel_dir,args.lineage_dir,args.output)

if __name__=="__main__":
    main()
