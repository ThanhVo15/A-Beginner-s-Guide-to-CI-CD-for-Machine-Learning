import pandas as pd
drug_df = pd.read_csv(r'Data\drug_data.csv')
drug_df =drug_df.sample(frac=1)
drug_df.head()


from sklearn.model_selection import train_test_split

X = drug_df.drop('Drug', axis=1)
y = drug_df.Drug.values

X_train,X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


cat_col = [1,2,3]
num_col = [0,4]

transform = ColumnTransformer(
    [
        ("encoder", OrdinalEncoder(), cat_col),
        ("num_imputer", SimpleImputer(strategy = "median"), num_col),
        ("num_sclaer", StandardScaler(), num_col)
    ]
)

pipe = Pipeline(
    steps = [
        ("preprocessing", transform),
        ("model", RandomForestClassifier(n_estimators=100, random_state=42))
    ]
)

pipe.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, f1_score

predictions = pipe.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average="macro")

print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

with open("Results/metrics.txt", "w") as outfile:
    outfile.write(f"\nAccuracy = {round(accuracy, 2)}, F1 Score = {round(f1, 2)}.")

    import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

cm = confusion_matrix(y_test, predictions, labels=pipe.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipe.classes_)
disp.plot()
plt.savefig("Results/model_results.png", dpi=120)

# !pip install skops
import skops.io as sio

sio.dump(pipe, "Model/drug_pipeline.skops")

from skops.io import get_untrusted_types
import skops.io as sio

# Identify untrusted types from the specific file
untrusted_types = get_untrusted_types(file="Model/drug_pipeline.skops")

# Load the model, using the identified untrusted types as trusted
pipeline = sio.load("Model/drug_pipeline.skops", trusted=untrusted_types)