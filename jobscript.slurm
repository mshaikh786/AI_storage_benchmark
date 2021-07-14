#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --tasks-per-node=8
#SBATCH --cpus-per-task=15
#SBATCH --time=02:00:00
#SBATCH --constraint=rome
#SBATCH --mem=400G

source ~/miniconda3/bin/activate torch_prof2
echo "Hostnames: $SLURM_NODELIST"


# Please edit your path to the dataset here:   
export DATA_DIR="/ibex/scratch/shaima0d/ML_framework_testing/ml_datasets/stripe_4/tiny-imagenet-200/train"



batch_size=1024
epochs=5
workers=${SLURM_CPUS_PER_TASK}
reps=1

cat << EOF > raw.output
Hostname: $(/bin/hostname)
Data source: $DATA_DIR 
Using Batch size : $batch_size
Epochs : $epochs
CPU workers: $workers
EOF

 
srun -n $SLURM_NTASKS -N $SLURM_NNODES -c $SLURM_CPUS_PER_TASK --mem-bind=local ./dload.py --dataDir=$DATA_DIR --num_workers=$workers --reps=$reps --batch_size=$batch_size >> raw.output



