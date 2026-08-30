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
