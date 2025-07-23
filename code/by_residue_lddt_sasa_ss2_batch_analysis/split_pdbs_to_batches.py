import os
import shutil
import sys

def split_pdbs(input_dir, output_dir, batch_size=1000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdb_files = [f for f in os.listdir(input_dir) if f.endswith('.pdb')]
    
    for i, pdb_file in enumerate(pdb_files):
        batch_num = i // batch_size
        batch_dir = os.path.join(output_dir, f'batch_{batch_num}')
        
        if not os.path.exists(batch_dir):
            os.makedirs(batch_dir)
        
        shutil.copy(os.path.join(input_dir, pdb_file), os.path.join(batch_dir, pdb_file))

    return len(pdb_files) // batch_size + 1  # Total number of batches

# Usage
input_dir = sys.argv[1]
batch_dir = sys.argv[2]

total_batches = split_pdbs(input_dir, batch_dir)
print(f"Total number of batches: {total_batches}")
