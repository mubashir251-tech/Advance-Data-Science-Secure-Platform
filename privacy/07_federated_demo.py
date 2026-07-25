"""Demo 3d — Federated Learning simulation with Flower (3 clients, sklearn).
No data ever leaves a client; only model weights are aggregated."""
import flwr as fl, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/loans.csv")
df["g"] = (df["gender"] == "M").astype(int)
X = df[["age","income","credit_score","g"]].to_numpy()
y = df["approved"].to_numpy()
X = (X - X.mean(0)) / X.std(0)
parts = np.array_split(np.arange(len(X)), 3)

def get_params(m): return [m.coef_, m.intercept_]
def set_params(m, p): m.coef_, m.intercept_ = p[0], p[1]; return m

def client_fn(cid: str):
    idx = parts[int(cid)]
    Xtr, Xte, ytr, yte = train_test_split(X[idx], y[idx], test_size=0.2, random_state=0)
    model = LogisticRegression(max_iter=200, warm_start=True)
    model.fit(Xtr[:10], ytr[:10])     # init shape
    class C(fl.client.NumPyClient):
        def get_parameters(self, cfg): return get_params(model)
        def fit(self, p, cfg):
            set_params(model, p); model.fit(Xtr, ytr)
            return get_params(model), len(Xtr), {}
        def evaluate(self, p, cfg):
            set_params(model, p)
            acc = model.score(Xte, yte)
            return float(1-acc), len(Xte), {"accuracy": acc}
    return C().to_client()

fl.simulation.start_simulation(
    client_fn=client_fn, num_clients=3,
    config=fl.server.ServerConfig(num_rounds=3))
