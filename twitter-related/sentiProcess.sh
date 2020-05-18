#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=2
module load Python/3.4.3-goolf-2015a
#module load Java/1.8.0_71
#module load mpj/0.44
time srun -n 4 python sentiAnalysisMPI.py


