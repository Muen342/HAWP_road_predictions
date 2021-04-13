#!/bin/bash
#SBATCH --account=def-jzelek
#SBATCH --gres=gpu:2       
#SBATCH --mem-per-cpu=16000M    
#SBATCH --time=0-04:00     
#SBATCH --cpus-per-task=1  
#SBATCH --output=%N-%j.out

module load StdEnv/2020
module load python/3.6
python create_llamas_train.py