import sys
import os
from Bio import PDB
from Bio.PDB.SASA import ShrakeRupley
import pandas as pd
import numpy as np

def analyze_pdb(pdb_file):
    # Initialize parser and structure
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_file)

    # Initialize SASA calculator
    sr = ShrakeRupley()

    # Calculate SASA for the whole structure
    sr.compute(structure, level="S")
    total_sasa = sum(atom.sasa for atom in structure.get_atoms())

    # Prepare data for the table
    data = []

    # Calculate SASA for each residue
    sr.compute(structure, level="R")

    for model in structure:
        for chain in model:
            for residue in chain:
                if PDB.is_aa(residue):
                    res_id = residue.get_id()
                    res_num = res_id[1]
                    res_name = residue.get_resname()
                    
                    # Calculate SASA for the residue
                    residue_sasa = sum(atom.sasa for atom in residue)
                    
                    # Get LDDT (B-factor) for CA atom
                    ca_atom = residue['CA']
                    lddt = ca_atom.get_bfactor() if ca_atom else np.nan

                    data.append([res_num, res_name, residue_sasa, lddt])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['residue_number', 'residue_name', 'residue_sasa', 'residue_lddt'])
    
    # Round numeric columns to two decimal places
    df['residue_sasa'] = df['residue_sasa'].round(2)
    df['residue_lddt'] = df['residue_lddt'].round(2)

    # Validate SASA calculation
    sum_residue_sasa = df['residue_sasa'].sum()
    print(f"Sum of residue SASA: {sum_residue_sasa:.2f}")
    print(f"Total structure SASA: {total_sasa:.2f}")
    print(f"Difference: {abs(sum_residue_sasa - total_sasa):.2f}")

    return df

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_pdb_file> <output_tsv_path>")
        sys.exit(1)

    pdb_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(pdb_file):
        print(f"Error: File '{pdb_file}' not found.")
        sys.exit(1)

    result_df = analyze_pdb(pdb_file)

    # Save to TSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    result_df.to_csv(output_file, sep='\t', index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
