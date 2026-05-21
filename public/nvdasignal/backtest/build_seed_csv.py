"""
build_seed_csv.py  — generates memory_cycle_data.csv (the editable input)

Encodes the documented anchor points for two memory cycles and writes a tidy
monthly CSV. REPLACE the dram_spot / dram_contract / nand_contract columns with
your real TrendForce series and (optionally) mu_stock with real monthly closes,
then re-run backtest_engine.py.

Provenance: MU revenue & gross-margin anchors are from Micron 8-K filings;
turning-point DATES are exact; price indices are normalized shapes (100 = each
cycle's peak) and stock levels are approximate monthly closes for shape.
"""
import numpy as np, pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def monthly(start, n):
    return [start + relativedelta(months=i) for i in range(n)]

def step_quarterly(dates, anchors):
    """anchors: {YYYY-MM: value} assigned at report month, held forward/back."""
    s = pd.Series(index=dates, dtype=float)
    for k, val in anchors.items():
        dt = datetime.strptime(k, "%Y-%m")
        if dt in s.index:
            s.loc[dt] = val
    return s.ffill().bfill()

rows = []

# ===================== CYCLE 2018-19 =====================
d = monthly(datetime(2017, 9, 1), 31)  # 2017-09 .. 2020-03
stock = [35,41,44,41, 43,46,53,50,58,52,54,51,46,40,39,32,  # ..2018-12 (peak May, trough Dec)
         36,40,41,46,39,39,47,45,49,46,47,54, 58,54,44]       # 2019 + 2020Q1
dram  = [90,93,96,98, 99,100,100,100,100,100,99,98,96,92,88,84,  # peak plateau mid-2018
         78,72,67,63,60,58,56,55,55,56,57,58, 60,62,63]           # decel late-2019 -> recover
nand  = [88,91,94,96, 98,100,100,99,98,96,93,90,86,82,78,74,
         70,66,62,59,57,56,56,57,58,60,62,64, 66,68,70]
rev = step_quarterly(d, {"2018-11":7.91, "2019-02":5.84, "2019-05":4.79,
                          "2019-08":4.87, "2019-11":5.14, "2020-02":4.80,
                          "2017-11":6.80, "2018-02":7.35, "2018-05":7.80, "2018-08":8.44})
gm  = step_quarterly(d, {"2018-11":59, "2019-02":50, "2019-05":39, "2019-08":31,
                          "2019-11":27, "2020-02":29, "2018-02":58, "2018-05":61, "2018-08":61,
                          "2017-11":55})
events = {datetime(2018,12,1):"broad-market + cycle bottom", datetime(2019,9,1):"price-decline decelerates (recovery tell)"}
for i, dt in enumerate(d):
    rows.append(dict(date=dt.strftime("%Y-%m"), cycle="2018-19", dram_spot="", dram_contract=dram[i],
                     nand_contract=nand[i], mu_stock=stock[i], mu_revenue=round(float(rev.iloc[i]),2),
                     mu_gross_margin=round(float(gm.iloc[i]),1), event=events.get(dt,"")))

# ===================== CYCLE 2021-24 =====================
d = monthly(datetime(2021, 1, 1), 42)  # 2021-01 .. 2024-06
stock = [75,82,88,90,84,80,76,73,74,71,78,85,
         96,90,78,70,71,55,57,60,50,49,56,50,
         60,58,60,63,66,63,66,70,68,70,78,85,
         90,95,105,118,110,120]
dram  = [82,86,90,94,97,99,100,100,98,94,90,85,
         80,74,68,64,60,56,52,49,47,46,46,47,
         48,50,52,55,58,60,62,64,66,69,72,76,
         80,84,88,92,95,98]
nand  = [85,88,92,95,98,100,100,99,96,92,88,84,
         80,75,70,66,62,58,54,51,49,48,48,49,
         50,52,54,56,59,61,63,65,67,70,73,77,
         81,85,89,93,96,99]
rev = step_quarterly(d, {"2021-02":6.20,"2021-05":7.40,"2021-08":8.30,"2021-11":7.70,
                          "2022-02":7.80,"2022-05":8.64,"2022-08":6.64,"2022-11":4.09,
                          "2023-02":3.69,"2023-05":3.75,"2023-08":4.01,"2023-11":4.73,
                          "2024-02":5.82,"2024-05":6.81})
gm  = step_quarterly(d, {"2021-02":32,"2021-05":42,"2021-08":47,"2021-11":47,
                          "2022-02":47,"2022-05":47.4,"2022-08":40,"2022-11":21,
                          "2023-02":-31.4,"2023-05":-16.1,"2023-08":-9,"2023-11":1,
                          "2024-02":19,"2024-05":28})
events = {datetime(2022,11,1):"wafer-cut capitulation (-20%)"}
for i, dt in enumerate(d):
    rows.append(dict(date=dt.strftime("%Y-%m"), cycle="2021-24", dram_spot="", dram_contract=dram[i],
                     nand_contract=nand[i], mu_stock=stock[i], mu_revenue=round(float(rev.iloc[i]),2),
                     mu_gross_margin=round(float(gm.iloc[i]),1), event=events.get(dt,"")))

df = pd.DataFrame(rows)
df.to_csv("/mnt/user-data/outputs/memory_cycle_data.csv", index=False)
print(f"Wrote {len(df)} rows across {df.cycle.nunique()} cycles.")
print(df.groupby('cycle').size().to_string())
