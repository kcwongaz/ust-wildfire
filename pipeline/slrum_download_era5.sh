#!/bin/bash

# NOTE: Lines starting with "#SBATCH" are valid SLURM commands or statements,
#       while those starting with "#" and "##SBATCH" are comments.  Uncomment
#       "##SBATCH" line means to remove one # and start with #SBATCH to be a
#       SLURM command or statement.


#SBATCH -J era5 #Slurm job name

# Set the maximum runtime, uncomment if you need it
##SBATCH -t 48:00:00 #Maximum runtime of 48 hours

# Enable email notificaitons when job begins and ends, uncomment if you need it
#SBATCH --mail-user=user@connect.ust.hk #Update your email address
#SBATCH --mail-type=begin
#SBATCH --mail-type=end

# Choose partition (queue) to use. Note: replace <partition_to_use> with the name of partition
#SBATCH -p cpu-share

# Use 1 nodes and 1 core
#SBATCH -N 1 -n 1

# Setup runtime environment if necessary
# For example, setup intel MPI environment
# module swap gnu8 intel

# Go to the job submission directory and run your application
cd $HOME/wildfire
source ./venv/bin/activate

python ./pipeline/download_era5/download_california.py
