#!/bin/bash
#SBATCH --account=def-jzelek
#SBATCH --gres=gpu:2       
#SBATCH --mem=8000M       
#SBATCH --time=0-00:30     
#SBATCH --cpus-per-task=4  
#SBATCH --output=%N-%j.out

module load StdEnv/2020
PATH2HAWP=/scratch/mezhang/hawp #use your own path
module load gcc/9.3.0 cuda scipy-stack opencv
virtualenv --no-download $SLURM_TMPDIR/hawp_env && . $SLURM_TMPDIR/hawp_env/bin/activate
pip  install --no-index torch==1.7.1 torchvision
pip install --no-index -r $PATH2HAWP/requirement.txt
python $PATH2HAWP/setup.py build_ext --inplace 
export PYTHONPATH=$PYTHONPATH:$PATH2HAWP
# use figures that you have imported into the figures folder
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/21000.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/32000.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/53000.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/56000.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/1418941858_0783285000_color_rect.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/1418942007_0665705000_color_rect.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/1418941877_0385639000_color_rect.png
python scripts/predict.py --config-file config-files/hawp.yaml --img figures/1419279916_0084518000_color_rect.png

