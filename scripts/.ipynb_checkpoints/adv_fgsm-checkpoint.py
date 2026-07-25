"""FGSM + PGD evasion with ART on a small TF2/Keras model."""
import json
import pathlib
import numpy as np
import tensorflow as tf

from art.estimators.classification import TensorFlowV2Classifier
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent
from _common import load

# Ensure TF2 eager execution (default in TF 2.x)
tf.config.run_functions_eagerly(True)

# 1. Load and normalize data
(X_tr, X_te, y_tr, y_te), _ = load()
X_tr = X_tr.astype("float32")
X_te = X_te.astype("float32")

mu = X_tr.mean(axis=0)
sd = X_tr.std(axis=0) + 1e-6
X_tr = (X_tr - mu) / sd
X_te = (X_te - mu) / sd

num_classes = 2
y_tr_oh = tf.keras.utils.to_categorical(y_tr, num_classes)
y_te_oh = tf.keras.utils.to_categorical(y_te, num_classes)

# 2. Define a small Keras model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_tr.shape[1],)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(num_classes, activation="softmax"),
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=["accuracy"],
)

model.fit(X_tr, y_tr_oh, epochs=6, batch_size=128, verbose=0)

# 3. Wrap in ART TensorFlowV2Classifier
loss_object = tf.keras.losses.CategoricalCrossentropy()

classifier = TensorFlowV2Classifier(
    model=model,
    nb_classes=num_classes,
    input_shape=(X_tr.shape[1],),
    loss_object=loss_object,
    clip_values=(float(X_tr.min()), float(X_tr.max())),
)

# 4. Evaluate on clean test data
pred_clean = classifier.predict(X_te)
clean_acc = float((np.argmax(pred_clean, axis=1) == y_te).mean())

# 5. FGSM attack
fgsm_attack = FastGradientMethod(estimator=classifier, eps=0.1)
X_te_fgsm = fgsm_attack.generate(x=X_te)
pred_fgsm = classifier.predict(X_te_fgsm)
fgsm_acc = float((np.argmax(pred_fgsm, axis=1) == y_te).mean())

# 6. PGD attack
pgd_attack = ProjectedGradientDescent(
    estimator=classifier,
    eps=0.1,
    eps_step=0.02,
    max_iter=10,
)
X_te_pgd = pgd_attack.generate(x=X_te)
pred_pgd = classifier.predict(X_te_pgd)
pgd_acc = float((np.argmax(pred_pgd, axis=1) == y_te).mean())

# 7. Save and print results
out = {
    "clean_acc": clean_acc,
    "fgsm_acc": fgsm_acc,
    "pgd_acc": pgd_acc,
}

pathlib.Path("reports").mkdir(exist_ok=True)
pathlib.Path("reports/adversarial.json").write_text(json.dumps(out, indent=2))

print(json.dumps(out, indent=2))
