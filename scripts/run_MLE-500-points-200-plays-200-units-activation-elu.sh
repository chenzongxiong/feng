#!/bin/bash

#SBATCH -J run_MLE-nb_plays-200-units-200-activation-elu-batch-size-500-x
#SBATCH -D /home/zxchen/feng
#SBATCH -o ./tmp/run_MLE-nb_plays-200-units-200-activation-elu-batch-size-500-x.out
#SBATCH --nodes=1
#SBATCH --mem=80G
#SBATCH --time=30-00:00:00
#SBATCH --partition=big
#SBATCH --mail-type=end
#SBATCH --mail-user=czxczf@gmail.com

hostname
source /home/zxchen/.venv3/bin/activate
python run_MLE.py --__nb_plays__ 200 --__units__ 200 --__activation__ elu --batch_size 500
