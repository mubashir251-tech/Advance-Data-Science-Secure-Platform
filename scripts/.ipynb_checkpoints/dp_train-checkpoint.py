"""DP-SGD training with TensorFlow Privacy → reports a formal (ε, δ) budget."""
import argparse
import numpy as np
import tensorflow as tf
from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasSGDOptimizer
from tensorflow_privacy.privacy.analysis.compute_dp_sgd_privacy_lib import compute_dp_sgd_privacy
from _common import load

# Command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument("--epochs", type=int, default=5)
ap.add_argument("--noise-multiplier", type=float, default=1.1)
ap.add_argument("--l2-norm-clip", type=float, default=1.0)
ap.add_argument("--microbatches", type=int, default=16)
ap.add_argument("--batch-size", type=int, default=16)
a = ap.parse_args()

# Load and normalize data
(X_tr, X_te, y_tr, y_te), _ = load()
X_tr = X_tr.astype("float32")
X_te = X_te.astype("float32")

mu = X_tr.mean(0)
sd = X_tr.std(0) + 1e-6
X_tr = (X_tr - mu) / sd
X_te = (X_te - mu) / sd

# Build tf.data pipelines and drop partial batches
train_ds = tf.data.Dataset.from_tensor_slices((X_tr, y_tr))
train_ds = train_ds.shuffle(len(X_tr), seed=42).batch(a.batch_size, drop_remainder=True)

test_ds = tf.data.Dataset.from_tensor_slices((X_te, y_te)).batch(a.batch_size)

# Model definition
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_tr.shape[1],)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(2),
])

# DP-SGD optimizer
opt = DPKerasSGDOptimizer(
    l2_norm_clip=a.l2_norm_clip,
    noise_multiplier=a.noise_multiplier,
    num_microbatches=a.microbatches,
    learning_rate=0.05,
)

loss = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True,
    reduction=tf.keras.losses.Reduction.NONE,
)

model.compile(optimizer=opt, loss=loss, metrics=["accuracy"])

# Train with DP-SGD
model.fit(train_ds, epochs=a.epochs, verbose=2)

# Evaluate and compute epsilon
acc = model.evaluate(test_ds, verbose=0)[1]
eps, _ = compute_dp_sgd_privacy(
    n=len(X_tr),
    batch_size=a.batch_size,
    noise_multiplier=a.noise_multiplier,
    epochs=a.epochs,
    delta=1e-5,
)

print(f"\nDP test acc={acc:.3f}  Epsilon (δ=1e-5) = {eps:.2f}")
