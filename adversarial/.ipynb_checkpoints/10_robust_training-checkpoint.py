"""Demo 4c — Adversarial training: retrain on PGD examples and re-measure."""
import numpy as np, pandas as pd, tensorflow as tf
from sklearn.model_selection import train_test_split
from art.estimators.classification import KerasClassifier
from art.attacks.evasion import ProjectedGradientDescent
from art.defences.trainer import AdversarialTrainer
tf.compat.v1.disable_eager_execution()

df = pd.read_csv("data/loans.csv")
df["g"] = (df["gender"]=="M").astype(int)
X = df[["age","income","credit_score","g"]].astype("float32").to_numpy()
X = (X - X.mean(0))/X.std(0)
y = tf.keras.utils.to_categorical(df["approved"], 2)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0)

m = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation="relu", input_shape=(4,)),
    tf.keras.layers.Dense(2, activation="softmax")])
m.compile("adam", "categorical_crossentropy", metrics=["accuracy"])
clf = KerasClassifier(model=m, clip_values=(X.min(),X.max()), use_logits=False)

trainer = AdversarialTrainer(clf,
    attacks=ProjectedGradientDescent(clf, eps=0.2, max_iter=10), ratio=0.5)
trainer.fit(Xtr, ytr, nb_epochs=5, batch_size=64)

atk = ProjectedGradientDescent(clf, eps=0.2, max_iter=20)
adv = atk.generate(Xte)
clean = (clf.predict(Xte).argmax(1) == yte.argmax(1)).mean()
robust = (clf.predict(adv).argmax(1) == yte.argmax(1)).mean()
print(f"After robust training  clean={clean:.3f}  adversarial={robust:.3f}")
