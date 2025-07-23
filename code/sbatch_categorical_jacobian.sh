#!/bin/bash

#SBATCH --job-name=cat_jac           # Job name
#SBATCH --output=job_%j.out          # Standard output file (%j will be replaced by job ID)
#SBATCH --error=job_%j.err           # Standard error file
#SBATCH --time=36:00:00             # Time limit (HH:MM:SS)
#SBATCH --gres=gpu:1,vmem:20g       # Number of GPUs (1 in this case)
#SBATCH --mem=32G                   # Memory per node
#SBATCH --cpus-per-task=4          # Number of CPU cores

# Print some information about the job
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_JOB_NODELIST"
echo "Available GPUs: $CUDA_VISIBLE_DEVICES"

# Load any necessary modules (uncomment if needed)

ROOT="/sci/labs/fora/share/softwares/esmfold"
jac_script="/sci/labs/fora/share/softwares/categorical_jacobian/categorical_jacobian_esm1b_local_run.py"
mem_jac="/sci/labs/fora/share/softwares/categorical_jacobian/categorical_jacobian_esm1b_memory_efficient_run.py"
no_pssm_jac="/sci/labs/fora/share/softwares/categorical_jacobian/categorical_jacobian_no_pssm.py"
export PYTHONPATH=''
module load cuda/12.4.1 cudnn/9.1.0 nvidia #torch/1.11.0-cuda11.3
source $ROOT/bin/activate
export TORCH_HOME=$ROOT


# Run your Python script
# the categorical_jacobian script takes an argument which is the name of the relevant fasta file
input_file=$1

#!/bin/bash

script_flag=$2

case $script_flag in
 1)
   script_path=$jac_script
   ;;
 2)
   script_path=$mem_jac
   ;;
 3)
   script_path=$no_pssm_jac
   ;;
 *)
   echo "Invalid flag. Must be 1, 2, or 3"
   exit 1
   ;;
esac

echo $script_path

# -u flag disables Python's output buffering and allows real-time viewing of print statements.
/vol/ek/Home/tomertsa/miniforge3/envs/ace_coevolution/bin/python3 -u $script_path df $input_file

