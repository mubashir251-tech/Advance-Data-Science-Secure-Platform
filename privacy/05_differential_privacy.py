"""Demo 3b — Differential Privacy on aggregate statistics using OpenDP.
Computes a DP mean of income with ε=1.0."""
import opendp.prelude as dp, pandas as pd
dp.enable_features("contrib")

income = pd.read_csv("data/loans.csv")["income"].tolist()
bounds = (15_000.0, 200_000.0)
ctx = dp.Context.compositor(
    data=income,
    privacy_unit=dp.unit_of(contributions=1),
    privacy_loss=dp.loss_of(epsilon=1.0),
    split_evenly_over=1,
)
query = (
    ctx.query()
       .clamp(bounds).cast_default(float)
       .resize(size=len(income), constant=sum(bounds)/2)
       .mean()
       .laplace()
)
true_mean = sum(income)/len(income)
dp_mean   = query.release()
print(f"true mean   : {true_mean:,.2f}")
print(f"DP mean ε=1 : {dp_mean:,.2f}")
print(f"noise added : {dp_mean - true_mean:+.2f}")
