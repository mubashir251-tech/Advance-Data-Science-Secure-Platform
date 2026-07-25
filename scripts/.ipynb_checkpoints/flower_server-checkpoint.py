"""Flower FL server — 3 rounds, FedAvg with secure aggregation semantics."""
import flwr as fl

strategy = fl.server.strategy.FedAvg(
    min_available_clients=3,
    min_fit_clients=3,
)

fl.server.start_server(
    server_address="0.0.0.0:8088",
    config=fl.server.ServerConfig(num_rounds=3),
    strategy=strategy,
)
