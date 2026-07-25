"""Demo 3c — DP-SGD training with TensorFlow Privacy.
Trains a tiny MLP on the loans dataset with a guaranteed (ε,δ) budget."""
import numpy as np, pandas as pd, tensorflow as tf
from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import (
    DPKerasSGDOptimizer)
from tensorflow_privacy.privacy.analysis.compute_dp_sgd_privacy_lib import (
    compute_dp_sgd_privacy_statement)

df = pd.read_csv("data/loans.csv")
df["g"] = (df["gender"] == "M").astype(int)
X = df[["age", "income", "credit_score", "g"]].astype("float32").to_numpy()
X = (X - X.mean(0)) / X.std(0)
y = df["approved"].astype("float32").to_numpy()

BATCH, EPOCHS, L2, NM = 250, 3, 1.0, 1.1
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation="relu", input_shape=(4,)),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
opt = DPKerasSGDOptimizer(l2_norm_clip=L2, noise_multiplier=NM,
                          num_microbatches=BATCH, learning_rate=0.05)
loss = tf.keras.losses.BinaryCrossentropy(
    from_logits=False, reduction=tf.losses.Reduction.NONE)
model.compile(optimizer=opt, loss=loss, metrics=["accuracy"])
model.fit(X, y, epochs=EPOCHS, batch_size=BATCH, verbose=2)

print(compute_dp_sgd_privacy_statement(
    number_of_examples=len(X), batch_size=BATCH, num_epochs=EPOCHS,
    noise_multiplier=NM, delta=1e-5))
