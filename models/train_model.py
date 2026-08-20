import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import classification_report, confusion_matrix

import pickle
import os


# =======================================
# LOAD CLEAN DATASET
# =======================================

data = pd.read_csv(
    "data/complaint_dataset_clean.csv"
)

print("Dataset Loaded Successfully")

print("\nDataset Size:")
print(data.shape)

print("\nDepartment Distribution:")
print(data["department"].value_counts())


# =======================================
# SPLIT DATA
# =======================================

X = data["complaint_text"]
y = data["department"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =======================================
# MODEL 1 - NAIVE BAYES
# =======================================

nb_model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 3),
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            MultinomialNB()
        )
    ]
)


# =======================================
# MODEL 2 - LOGISTIC REGRESSION
# =======================================

lr_model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 3),
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000
            )
        )
    ]
)


# =======================================
# MODEL 3 - LINEAR SVM
# =======================================

svm_model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 3),
                sublinear_tf=True
            )
        ),
        (
            "classifier",
            LinearSVC()
        )
    ]
)


# =======================================
# TRAIN MODELS
# =======================================

print("\nTraining Multinomial Naive Bayes...")
nb_model.fit(X_train, y_train)

print("Training Logistic Regression...")
lr_model.fit(X_train, y_train)

print("Training Linear SVM...")
svm_model.fit(X_train, y_train)

print("\nAll Models Trained Successfully!")


# =======================================
# ACCURACY
# =======================================

nb_accuracy = nb_model.score(
    X_test,
    y_test
)

lr_accuracy = lr_model.score(
    X_test,
    y_test
)

svm_accuracy = svm_model.score(
    X_test,
    y_test
)


# =======================================
# MODEL COMPARISON
# =======================================

print("\n======================================")
print("MODEL COMPARISON")
print("======================================")

print(
    "Multinomial Naive Bayes:",
    round(nb_accuracy * 100, 2),
    "%"
)

print(
    "Logistic Regression:",
    round(lr_accuracy * 100, 2),
    "%"
)

print(
    "Linear SVM:",
    round(svm_accuracy * 100, 2),
    "%"
)


# =======================================
# LINEAR SVM PREDICTIONS
# =======================================

svm_predictions = svm_model.predict(
    X_test
)


# =======================================
# CLASSIFICATION REPORT
# =======================================

print("\n======================================")
print("CLASSIFICATION REPORT - LINEAR SVM")
print("======================================")

print(
    classification_report(
        y_test,
        svm_predictions
    )
)


# =======================================
# CONFUSION MATRIX
# =======================================

print("\n======================================")
print("CONFUSION MATRIX - LINEAR SVM")
print("======================================")


labels = sorted(
    y.unique()
)


cm = confusion_matrix(
    y_test,
    svm_predictions,
    labels=labels
)


print("\nDepartments:")
print(labels)

print("\nConfusion Matrix:")
print(cm)


# =======================================
# MISCLASSIFIED COMPLAINTS
# =======================================

results = pd.DataFrame(
    {
        "complaint_text": X_test.values,
        "actual": y_test.values,
        "predicted": svm_predictions
    }
)


misclassified = results[
    results["actual"] != results["predicted"]
]


print("\n======================================")
print("MISCLASSIFIED COMPLAINTS")
print("======================================")


if len(misclassified) == 0:

    print("No misclassified complaints!")

else:

    print(
        misclassified.to_string(
            index=False
        )
    )


# =======================================
# SELECT BEST MODEL
# =======================================

models = {
    "Naive Bayes": (
        nb_model,
        nb_accuracy
    ),

    "Logistic Regression": (
        lr_model,
        lr_accuracy
    ),

    "Linear SVM": (
        svm_model,
        svm_accuracy
    )
}


best_name = max(
    models,
    key=lambda name: models[name][1]
)


best_model = models[
    best_name
][0]


best_accuracy = models[
    best_name
][1]


# =======================================
# BEST MODEL
# =======================================

print("\n======================================")
print("BEST MODEL")
print("======================================")

print(
    "Model:",
    best_name
)

print(
    "Accuracy:",
    round(
        best_accuracy * 100,
        2
    ),
    "%"
)


# =======================================
# SAVE BEST MODEL
# =======================================

os.makedirs(
    "models",
    exist_ok=True
)


model_path = (
    "models/complaint_classifier.pkl"
)


with open(
    model_path,
    "wb"
) as file:

    pickle.dump(
        best_model,
        file
    )


print(
    "\n✅ Best Model Saved Successfully!"
)

print(
    "Saved Location:"
    model_path
)