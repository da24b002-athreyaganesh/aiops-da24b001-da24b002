Steps to run the code:

aws config
conda env create -f environment.yml
conda activate <env_name>


PARTNER A:
python script.py
dvc add data
dvc push
git add scripts.py environment.yml data.dvc .dvc/config .gitignore
git commit -m "your message"
git push origin main



PARTNER B:
PARTNER B:

git clone
cd 
git checkout 90e85f5
dvc pull
conda env create -f environment.yml
conda activate aiops
python script.py

Partner B validation accuracy: 0.9722
Partner A validation accuracy: 0.9722
Difference: 0.0000 , Successfully reproduced.
