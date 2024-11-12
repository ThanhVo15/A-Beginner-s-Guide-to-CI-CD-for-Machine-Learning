install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

format:
	black *.py

train:
	python train.py

eval:
	echo "## Model Metrics" > report.md
	cat ./Results/metrics.txt >> report.md
	
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	
	cml comment create report.md

commit:
	git commit -am "new changes"
	git push origin main

update-branch:
	git config user.name "$(USER_NAME)"
	git config user.email "$(USER_EMAIL)"
	git add report.md
	git commit -m "Update with new results"
	git push origin main



