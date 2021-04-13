
#!/bin/bash
#SBATCH --account=def-jzelek
#SBATCH --gres=gpu:2       
#SBATCH --mem=8000M       
#SBATCH --time=0-02:00     
#SBATCH --cpus-per-task=4  
#SBATCH --output=%N-%j.out

module load StdEnv/2020
PATH2HAWP=/project/def-jzelek/mezhang/hawp2 #use your own path
module load gcc/9.3.0 cuda scipy-stack opencv
virtualenv --no-download $SLURM_TMPDIR/hawp_env && . $SLURM_TMPDIR/hawp_env/bin/activate
pip  install --no-index torch==1.7.1 torchvision
pip install --no-index -r $PATH2HAWP/requirement.txt
python $PATH2HAWP/setup.py build_ext --inplace 
export PYTHONPATH=$PYTHONPATH:$PATH2HAWP

CUDA_VISIBLE_DEVICES=0, python scripts/test.py --config-file config-files/hawp.yaml [optional] --display
