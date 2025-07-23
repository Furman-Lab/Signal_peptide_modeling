import sys
import os
import pandas as pd

def parse_ss_file(ss_file_path):
    with open(ss_file_path, 'r') as file:
        content = file.read().strip()
    
    ss_string, pdb_filename = content.rsplit(None, 1)
    ss_string = ss_string.replace('-', 'C')  # Replace '-' with 'C'
    
    return list(ss_string), os.path.splitext(os.path.basename(pdb_filename))[0]

def combine_sasa_ss(sasa_file_path, ss_file_path, output_dir):
    # Read SASA data
    sasa_df = pd.read_csv(sasa_file_path, sep='\t')
    
    # Parse SS file
    ss_list, pdb_name = parse_ss_file(ss_file_path)
    
    # Ensure the number of residues match
    if len(sasa_df) != len(ss_list):
        print(f"Error: Number of residues in SASA file ({len(sasa_df)}) "
              f"does not match SS file ({len(ss_list)})")
        sys.exit(1)
    
    # Add SS data to SASA dataframe
    sasa_df['residue_ss'] = ss_list
    
    # Save combined data
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{pdb_name}_sasa_lddt_ss.tsv")
    sasa_df.to_csv(output_file, sep='\t', index=False)
    print(f"Combined data saved to {output_file}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_sasa_tsv> <path_to_ss_file> <output_directory>")
        sys.exit(1)

    sasa_file = sys.argv[1]
    ss_file = sys.argv[2]
    output_dir = sys.argv[3]
    
    combine_sasa_ss(sasa_file, ss_file, output_dir)

if __name__ == "__main__":
    main()
