"""Flower FL client — each client trains on a disjoint shard, raw data stays local."""
import sys, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
import flwr as fl
from _common import load

cid = int(sys.argv[1]); n_clients = 3
(X_tr, X_te, y_tr, y_te), _ = load()
idx = np.array_split(np.arange(len(X_tr)), n_clients)[cid]
Xc, yc = X_tr[idx], y_tr[idx]
model = LogisticRegression(max_iter=200, warm_start=True)
model.classes_ = np.array([0, 1])
model.coef_ = np.zeros((1, Xc.shape[1])); model.intercept_ = np.zeros(1)

def get_p(m): return [m.coef_, m.intercept_]
def set_p(m, p): m.coef_, m.intercept_ = p[0], p[1]

class C(fl.client.NumPyClient):
    def get_parameters(self, config): return get_p(model)
    def fit(self, parameters, config):
        set_p(model, parameters); model.fit(Xc, yc)
        return get_p(model), len(Xc), {}
    def evaluate(self, parameters, config):
        set_p(model, parameters)
        loss = log_loss(y_te, model.predict_proba(X_te), labels=[0,1])
        acc = (model.predict(X_te) == y_te).mean()
        return float(loss), len(X_te), {"accuracy": float(acc)}

fl.client.start_numpy_client(server_address="127.0.0.1:8088", client=C())
