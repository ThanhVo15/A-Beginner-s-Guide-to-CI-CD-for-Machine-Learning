# Install dependencies
install:
    pip install --upgrade pip && \
    	pip install -r requirements.txt

# Format Python code using black
format:
    black *.py

# Train model
train:
    python train.py

# Evaluate model and create report
eval:
    echo "## Model Metrics" > report.md
    cat ./Results/metrics.txt >> report.md
    
    echo '\n## Confusion Matrix Plot' >> report.md
    echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
    
    cml comment create report.md

# Commit and push changes to the main branch
commit:
    git commit -am "new changes"
    git push origin main

# Update branch and push the report
update-branch:
    git config user.name "$(USER_NAME)"
    git config user.email "$(USER_EMAIL)"
    git add report.md
    git commit -m "Update with new results"
    git push origin main

# Hugging Face login
hf-login:
    git pull origin update
    git switch update
    pip install -U "huggingface_hub[cli]"
    huggingface-cli login --token $(HF) --add-to-git-credential

# Push app and model files to Hugging Face
push-hub:
    huggingface-cli upload ThanhVo15/A-Beginner-s-Guide-to-CI-CD-for-Machine-Learning ./App --repo-type=space --commit-message="Sync App files"
    huggingface-cli upload ThanhVo15/A-Beginner-s-Guide-to-CI-CD-for-Machine-LearningModel ./Model /Model --repo-type=space --commit-message="Sync Model"
    huggingface-cli upload ThanhVo15/A-Beginner-s-Guide-to-CI-CD-for-Machine-Learning ./Results /Metrics --repo-type=space --commit-message="Sync Model"

# Deploy to Hugging Face
deploy: hf-login push-hub
