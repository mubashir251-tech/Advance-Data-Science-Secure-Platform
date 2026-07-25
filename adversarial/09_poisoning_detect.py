"""Demo 4b — Data-poisoning detection via Activation Clustering (ART)."""
import numpy as np, pandas as pd, tensorflow as tf
from art.estimators.classification import KerasClassifier
from art.defences.detector.poison import ActivationDefence
tf.compat.v1.disable_eager_execution()

df = pd.read_csv("data/loans.csv")
df["g"] = (df["gender"]=="M").astype(int)
X = df[["age","income","credit_score","g"]].astype("float32").to_numpy()
X = (X - X.mean(0))/X.std(0)
y = df["approved"].to_numpy()

# Poison: flip labels of 10 % of class-0 samples with a trigger pattern
poison_idx = np.where(y==0)[0][:len(y)//10]
Xp = X.copy(); yp = y.copy()
Xp[poison_idx, 0] += 3.0             # trigger feature
yp[poison_idx] = 1

m = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation="relu", input_shape=(4,)),
    tf.keras.layers.Dense(2, activation="softmax")])
m.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
m.fit(Xp, yp, epochs=5, batch_size=64, verbose=0)

clf = KerasClassifier(model=m, clip_values=(Xp.min(), Xp.max()), use_logits=False)
y_onehot = tf.keras.utils.to_categorical(yp, 2)
defence = ActivationDefence(clf, Xp, y_onehot)
report, is_clean = defence.detect_poison(nb_clusters=2, nb_dims=4, reduce="PCA")
detected = np.where(np.array(is_clean) == 0)[0]
overlap = len(set(detected) & set(poison_idx))
print(f"injected poison : {len(poison_idx)}")
print(f"flagged samples : {len(detected)}")
print(f"true positives  : {overlap}")
