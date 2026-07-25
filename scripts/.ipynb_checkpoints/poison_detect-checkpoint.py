"""Data-poisoning detection via ART Activation Clustering."""
import argparse
import numpy as np
import tensorflow as tf

from art.estimators.classification import TensorFlowV2Classifier
from art.defences.detector.poison import ActivationDefence
from _common import load

ap = argparse.ArgumentParser()
ap.add_argument("--poison-fraction", type=float, default=0.1)
args = ap.parse_args()

(X_tr, X_te, y_tr, y_te), _ = load()
X_tr = X_tr.astype("float32")
X_te = X_te.astype("float32")

mu = X_tr.mean(axis=0)
sd = X_tr.std(axis=0) + 1e-6
X_tr = (X_tr - mu) / sd
X_te = (X_te - mu) / sd

rng = np.random.default_rng(0)
n_p = int(args.poison_fraction * len(X_tr))
idx = rng.choice(len(X_tr), n_p, replace=False)

y_poisoned = y_tr.copy()
y_poisoned[idx] = 1 - y_poisoned[idx]
y_oh = tf.keras.utils.to_categorical(y_poisoned, 2)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_tr.shape[1],)),
    tf.keras.layers.Dense(32, activation="relu", name="hidden"),
    tf.keras.layers.Dense(2, activation="softmax"),
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=["accuracy"],
)

model.fit(X_tr, y_oh, epochs=5, batch_size=128, verbose=0)

classifier = TensorFlowV2Classifier(
    model=model,
    nb_classes=2,
    input_shape=(X_tr.shape[1],),
    loss_object=tf.keras.losses.CategoricalCrossentropy(),
    clip_values=(float(X_tr.min()), float(X_tr.max())),
)

defence = ActivationDefence(classifier, X_tr, y_oh)
defence.detect_poison(nb_clusters=2, nb_dims=10, reduce="PCA")

is_clean = defence.is_clean_lst
flagged = np.where(np.array(is_clean) == 0)[0]

truth = set(idx.tolist())
pred = set(flagged.tolist())

tp = len(truth & pred)
fp = len(pred - truth)
fn = len(truth - pred)

prec = tp / max(tp + fp, 1)
rec = tp / max(tp + fn, 1)

print(f"poisoned={n_p}  flagged={len(flagged)}  precision={prec:.2f}  recall={rec:.2f}")
