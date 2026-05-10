"""
Generate three attack files for Activity #2.

Each file is a copy of clean engine 17 data (a representative engine that
spans the full Healthy → Caution → Critical degradation curve), but one
sensor channel has been manipulated.

Attack A — Sensor 11 (Ps30): constant drift +1.5 standard deviations
Attack B — Sensor 14 (NRc):  stuck-at value (frozen at cycle-30 reading)
Attack C — Sensor 9  (Nc):   gaussian noise injection σ = 0.3 * channel_std

Outputs are written to ../data/attack_{A,B,C}.csv

Usage:  python scripts/generate_attack_files.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TRAIN_PATH = ROOT / "data" / "train_FD001.txt"
OUT_DIR = ROOT / "data"

COLS = ["engine_id", "cycle"] + [f"op{i}" for i in range(1, 4)] + [f"s{i}" for i in range(1, 22)]


def load_engine(engine_id: int) -> pd.DataFrame:
    df = pd.read_csv(TRAIN_PATH, sep=r"\s+", header=None, names=COLS)
    return df[df["engine_id"] == engine_id].reset_index(drop=True).copy()


def main() -> None:
    rng = np.random.default_rng(42)
    base = load_engine(17)

    # Save a clean reference for diff-based explanations
    base.to_csv(OUT_DIR / "engine17_clean.csv", index=False)

    # ATTACK A — drift on Sensor 11 (Ps30)
    a = base.copy()
    a["s11"] = a["s11"] + 1.5 * a["s11"].std()
    a.to_csv(OUT_DIR / "attack_A.csv", index=False)

    # ATTACK B — stuck-at on Sensor 14 (NRc), frozen at cycle 30
    b = base.copy()
    if len(b) > 30:
        frozen_value = b.loc[30, "s14"]
        b["s14"] = frozen_value
    b.to_csv(OUT_DIR / "attack_B.csv", index=False)

    # ATTACK C — gaussian noise on Sensor 9 (Nc)
    c = base.copy()
    sigma = 0.3 * c["s9"].std()
    c["s9"] = c["s9"] + rng.normal(0.0, sigma, size=len(c))
    c.to_csv(OUT_DIR / "attack_C.csv", index=False)

    print("Wrote:")
    for name in ["engine17_clean.csv", "attack_A.csv", "attack_B.csv", "attack_C.csv"]:
        print(f"  {OUT_DIR / name}")


if __name__ == "__main__":
    main()
