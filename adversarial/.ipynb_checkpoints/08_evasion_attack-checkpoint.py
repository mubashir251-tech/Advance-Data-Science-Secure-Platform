"""Demo 4a — Evasion attacks (FGSM + PGD) with ART on a Keras classifier."""
import numpy as np, pandas as pd, tensorflow as tf
from sklearn.model_selection import train_test_split
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent
tf.compat.v1.disable_eager_execution()

df = pd.read_csv("data/loans.csv")
df["g"] = (df["gender"] == "M").astype(int)
X = df[["age","income","credit_score","g"]].astype("float32").to_numpy()
X = (X - X.mean(0)) / X.std(0)
y = tf.keras.utils.to_categorical(df["approved"], 2)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0)

m = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation="relu", input_shape=(4,)),
    tf.keras.layers.Dense(2, activation="softmax")])
m.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
m.fit(Xtr, ytr, epochs=5, batch_size=64, verbose=0)

clf = KerasClassifier(model=m, clip_values=(X.min(), X.max()), use_logits=False)
clean_acc = (clf.predict(Xte).argmax(1) == yte.argmax(1)).mean()

for name, atk in [("FGSM", FastGradientMethod(clf, eps=0.2)),
                  ("PGD",  ProjectedGradientDescent(clf, eps=0.2, max_iter=20))]:
    adv = atk.generate(x=Xte)
    acc = (clf.predict(adv).argmax(1) == yte.argmax(1)).mean()
    print(f"{name:5s}  clean={clean_acc:.3f}  adversarial={acc:.3f}")
