import os
import argparse

def split_fasta(input_file, chunk_size=1000):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = f"fasta_chunks_{base_name}"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_file, 'r') as f:
        chunk_num = 1
        seq_count = 0
        current_chunk = []
        
        for line in f:
            if line.startswith('>'):
                if seq_count == chunk_size:
                    write_chunk(output_dir, base_name, chunk_num, current_chunk)
                    current_chunk = []
                    seq_count = 0
                    chunk_num += 1
                seq_count += 1
            current_chunk.append(line.strip())
        
        # Write the last chunk if it's not empty
        if current_chunk:
            write_chunk(output_dir, base_name, chunk_num, current_chunk)

def write_chunk(output_dir, base_name, chunk_num, chunk_data):
    output_file = os.path.join(output_dir, f"{base_name}_chunk_{chunk_num}.fasta")
    with open(output_file, 'w') as f:
        f.write('\n'.join(chunk_data) + '\n')
    print(f"Wrote {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Split a FASTA file into chunks of sequences.")
    parser.add_argument("input_file", help="Input FASTA file to split")
    parser.add_argument("-s", "--chunk_size", type=int, default=1000, help="Number of sequences per chunk (default: 1000)")
    
    args = parser.parse_args()
    
    split_fasta(args.input_file, args.chunk_size)

if __name__ == "__main__":
    main()
