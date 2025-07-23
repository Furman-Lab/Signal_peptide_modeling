#!/usr/bin/bash

#SBATCH --get-user-env
#SBATCH --mail-user=tomer.tsaban@gmail.com
#SBATCH --mail-type=ALL,TIME_LIMIT_80

#SBATCH --job-name=fasta_process
#SBATCH --output=fasta_process_%A_%a.out
#SBATCH --error=fasta_process_%A_%a.err
#SBATCH --array=1-250%30
#SBATCH --time=50:00:00
#SBATCH --mem=4G

# Get the list of FASTA files
FASTA_FILES=(*.fasta)

# Calculate the index
INDEX=$((SLURM_ARRAY_TASK_ID - 1))

# Get the FASTA file for this job
FASTA_FILE=${FASTA_FILES[$INDEX]}

export PATH="path/to/signalp6/signalp6_venv/bin:$PATH"

# or use the signalp project venv 
echo `which python3`
echo `/usr/bin/python3 --version`
source /path/to/signalp6/signalp6_venv/bin/activate

echo `which python3`
echo `pip list`

signalp6 --fastafile "$FASTA_FILE" --organism eukarya --output_dir output\_"$FASTA_FILE" --format txt --mode slow-sequential

echo "done!"

