#!/usr/bin/env python3
"""Quick test for the SPI drought-analysis workflow.

This script verifies that the installation works and reproduces the core
Standardized Precipitation Index (SPI) computation used in the manuscript,
on a small *synthetic* precipitation series. It does NOT reproduce the full
manuscript results, because the original GPM IMERG, DEM, and KMA ASOS/AWS
datasets are subject to the data providers' access policies.

What it does
------------
1. Builds a synthetic monthly precipitation series (deterministic, seeded).
2. Computes SPI at 3/6/9/12-month accumulation windows using the same
   gamma-fit -> standard-normal transform as the main analysis.
3. Writes the result to ``results/quick_test/spi_quick_test.csv`` and prints
   a short summary so the run can be checked at a glance.

Usage
-----
    python examples/quick_test.py

Dependencies: numpy, pandas, scipy (all in requirements.txt).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import gamma, norm


def make_synthetic_precipitation(n_years: int = 30, seed: int = 42) -> pd.Series:
    """Return a seeded synthetic monthly precipitation series (mm).

    A simple seasonal cycle (wet summer / dry winter) plus gamma-distributed
    noise — enough to exercise the SPI fitting code deterministically.
    """
    rng = np.random.default_rng(seed)
    months = np.arange(n_years * 12)
    seasonal = 90.0 + 70.0 * np.sin(2 * np.pi * (months % 12) / 12.0)
    noise = rng.gamma(shape=2.0, scale=20.0, size=months.size)
    precip = np.clip(seasonal + noise - 40.0, 0.0, None)
    index = pd.date_range("1994-01-01", periods=months.size, freq="MS")
    return pd.Series(precip, index=index, name="precip_mm")


def compute_spi(precip: pd.Series, window: int) -> pd.Series:
    """Compute SPI for one accumulation window.

    Steps: rolling accumulation -> gamma fit on positive values (with a
    zero-precip correction) -> probability -> standard-normal quantile.
    """
    accum = precip.rolling(window=window, min_periods=window).sum()
    valid = accum.dropna()

    positive = valid[valid > 0]
    # Probability of zero precipitation (handled separately from the gamma fit).
    q0 = float((valid <= 0).mean())

    # floc=0 fixes the gamma location at 0, standard for SPI.
    shape, loc, scale = gamma.fit(positive, floc=0)

    cdf = q0 + (1.0 - q0) * gamma.cdf(valid, shape, loc=loc, scale=scale)
    cdf = np.clip(cdf, 1e-6, 1 - 1e-6)
    spi = pd.Series(norm.ppf(cdf), index=valid.index, name=f"SPI{window}")
    return spi.reindex(precip.index)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "results" / "quick_test"
    out_dir.mkdir(parents=True, exist_ok=True)

    precip = make_synthetic_precipitation()
    result = pd.DataFrame({"precip_mm": precip})
    for window in (3, 6, 9, 12):
        result[f"SPI{window}"] = compute_spi(precip, window)

    out_path = out_dir / "spi_quick_test.csv"
    result.to_csv(out_path, float_format="%.4f")

    print("Quick test completed successfully.")
    print(f"  synthetic months : {len(precip)}")
    print(f"  SPI windows      : 3, 6, 9, 12 month")
    print(f"  output written   : {out_path.relative_to(repo_root)}")
    print()
    print("Last 6 months (SPI values):")
    with pd.option_context("display.width", 120):
        print(result[["SPI3", "SPI6", "SPI9", "SPI12"]].tail(6).round(3).to_string())


if __name__ == "__main__":
    main()
