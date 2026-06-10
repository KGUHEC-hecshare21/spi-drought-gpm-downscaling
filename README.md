# High-resolution drought assessment using conditional GAN downscaling of GPM IMERG precipitation over Jeju Island

This repository provides the source code, preprocessing scripts, an example
quick-test workflow, and evaluation scripts associated with the manuscript:

> **A computational framework for high-resolution drought assessment using
> conditional GAN downscaling of GPM IMERG precipitation over Jeju Island.**

The workflow covers GPM IMERG preprocessing, conditional GAN (cGAN)-based
precipitation downscaling, Standardized Precipitation Index (SPI) calculation,
a Co-Kriging reference comparison, and drought evaluation over Jeju Island,
South Korea.

## Overview

- **Input**: GPM IMERG precipitation, downscaled to 0.01° by a conditional GAN
  and, as a geostatistical reference, by Co-Kriging
- **Method**: SPI calculation at 3-, 6-, 9-, and 12-month accumulation windows
- **Comparison**: cGAN-based SPI vs. Co-Kriging-based SPI vs. station observations
- **Evaluation**: RMSE, correlation, POD, FAR, and elevation-dependent analysis
- **Study area**: Jeju Island, South Korea
- **Periods**: 2004–2023 (daily), 2016–2023 (SPI validation)

## Repository structure

```
.
├── code/
│   ├── 01_gpm_preprocessing.ipynb     # GPM IMERG + station preprocessing
│   ├── 02_gan_downscaling.ipynb       # conditional GAN precipitation downscaling
│   ├── 03_spi_calculation.ipynb       # SPI computation (3/6/9/12 month)
│   ├── 04_spi_multiscale.ipynb        # multi-window SPI generation
│   ├── 05_statistical_analysis.ipynb  # main statistical analysis & comparison
│   ├── 06_spi_2004_validation.ipynb   # SPI validation for the 2004 period
│   ├── plot_spi_comparison.py         # SPI comparison plots
│   ├── plot_spi_heatmap.py            # SPI heatmap visualization
│   ├── plot_spi_heatmap_real_data.py  # SPI heatmap with observed data
│   ├── plot_jeju_watershed_map.py     # Jeju watershed / study-area map
│   ├── config.json                    # analysis configuration
│   └── archive/                       # earlier exploratory / iteration notebooks
│
├── examples/
│   └── quick_test.py                  # minimal runnable SPI quick test
│
├── results/
│   ├── figures/
│   │   ├── overview/                   # SPI comparison summary plots
│   │   ├── 2004/                       # 2004 period: metrics, correlation, POD, FAR
│   │   ├── 2004_heatmap/               # drought-category heatmaps
│   │   └── 2016/                       # 2016 period comparison
│   ├── spi/
│   │   ├── 2016/
│   │   │   ├── gan/                    # SPI from cGAN-downscaled precip (3/6/9/12 month)
│   │   │   └── cokriging/              # SPI from Co-Kriging-downscaled precip
│   │   └── gan_summary/                # cGAN SPI aggregated outputs
│   ├── quick_test/                     # output of examples/quick_test.py
│   ├── SPI_comparison_all_windows.csv
│   └── MinMaxAvg.xlsx
│
├── requirements.txt
└── LICENSE
```

## Installation

```bash
pip install -r requirements.txt
```

## Quick test

A minimal quick-test example is provided to verify the installation and the
core SPI calculation workflow. It runs on a small, deterministic **synthetic**
precipitation series and requires no external data:

```bash
python examples/quick_test.py
```

The script computes SPI at the 3/6/9/12-month windows and writes the output to:

```
results/quick_test/spi_quick_test.csv
```

This quick test does **not** reproduce the full manuscript results, because the
original GPM IMERG, DEM, and KMA ASOS/AWS datasets are subject to the data
providers' access policies (see *Code and data availability* below).

## Code and data availability

- **Code**: all preprocessing, downscaling, SPI, and evaluation scripts used in
  the manuscript are contained in this repository (`code/`). Earlier
  exploratory and iteration notebooks are kept under `code/archive/` for
  transparency.
- **Data**: the GPM IMERG precipitation, SRTM/DEM elevation, and KMA ASOS/AWS
  station observations are publicly distributed by their respective providers
  under their own access policies and are therefore not redistributed here. The
  derived SPI fields used in the analysis are included under `results/spi/`.

## Requirements

See [`requirements.txt`](requirements.txt). Core dependencies: `numpy`,
`pandas`, `scipy`, `xarray`, `netCDF4`, `rasterio`, `geopandas`,
`scikit-learn`, `matplotlib`, `seaborn`.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE).
