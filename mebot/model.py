from joblib import load, dump
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
import pandas as pd

model = load("mlp.joblib")

classes = [
    "Animal",
    "Color",
    "Fruit",
    "Part_Body",
    "Person",
    "Vegetable",
    "Counting",
    "Property",
    "Place",
    "Instrument",
    "Game",
]

# init the thing

things = pd.read_csv("classification.csv")
things.Names = things.Names.str.lower()

X = things.Names

cv = CountVectorizer()
Xf = cv.fit_transform(X)

# uncomment to train
# model = MLPClassifier(max_iter=1000)
# model.fit(Xf, y)
# dump(model, "mlp.joblib")
# print("ML Perceptron Score:", model.score(Xf, y))


def predict(text):
    """ predict pipeline """
    text = text.lower()

    # see if its in training set
    if X[X.isin([text])].empty:
        return "Node"

    text = [text]
    test = cv.transform(text)
    y = model.predict(test)
    y = y[0]  # single test
    return classes[y]


if __name__ == "__main__":
    #
    # testing
    print("Class:", predict("Phone"))
