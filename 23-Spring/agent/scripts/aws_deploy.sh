mv requirements.txt requirements_temp.txt
sam build --skip-pull-image
sam deploy --no-progressbar
mv requirements_temp.txt requirements.txt