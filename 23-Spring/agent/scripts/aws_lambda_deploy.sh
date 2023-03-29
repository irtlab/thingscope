mv requirements.txt requirements_temp.txt
sam build --skip-pull-image -t lambda_template.yaml
sam deploy --no-progressbar
mv requirements_temp.txt requirements.txt