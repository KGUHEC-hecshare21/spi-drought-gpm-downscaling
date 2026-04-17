# SPI Drought Analysis using GPM Downscaled Precipitation

Standardized Precipitation Index (SPI) drought analysis over Jeju Island using spatially downscaled GPM satellite precipitation data (GAN vs CoKriging).

This study applies the downscaled precipitation outputs from [gpm-precipitation-downscaling](https://github.com/KGUHEC-hecshare21/gpm-precipitation-downscaling) to evaluate drought characteristics through SPI at multiple time scales.

## Overview

- **Input**: GPM IMERG precipitation downscaled by GAN and CoKriging (0.01 deg)
- **Method**: SPI calculation at 3, 6, 9, and 12-month windows
- **Comparison**: GAN-based SPI vs CoKriging-based SPI vs station observations
- **Evaluation**: RMSE, Correlation, POD, FAR, elevation-dependent analysis
- **Study area**: Jeju Island, South Korea
- **Periods**: 2004-2023 (daily), 2016-2023 (SPI validation)

## Repository Structure

```
.
├── code/                              # All research code
│   ├── GPM_Preprocessing.ipynb         # GPM data preprocessing
│   ├── SPI_Calculation.ipynb           # SPI computation (3/6/9/12 month)
│   ├── SPI_2004.ipynb                  # SPI analysis for 2004 period
│   ├── Analysis.ipynb                  # Main statistical analysis
│   ├── 202506.ipynb                    # Extended analysis
│   ├── 2004.ipynb                      # 2004 data processing
│   ├── Conferece(png_0516).ipynb       # Conference figure generation
│   ├── plot_SPI_comparison_enhanced.py # SPI comparison plots
│   ├── plot_SPI_heatmap_enhanced.py    # SPI heatmap visualization
│   ├── plot_SPI_heatmap_with_real_data.py
│   └── plot_jeju_watershed_map_enhanced.py
│
├── results/
│   ├── figures/
│   │   ├── overview/                   # SPI comparison summary plots
│   │   ├── 2004/                       # 2004 period: metrics, correlation, POD, FAR
│   │   ├── 2004_heatmap/               # Drought category heatmaps
│   │   └── 2016/                       # 2016 period comparison
│   ├── spi/
│   │   ├── 2016/
│   │   │   ├── gan/                    # SPI from GAN-downscaled precip (3/6/9/12 month)
│   │   │   └── cokriging/              # SPI from CoKriging-downscaled precip
│   │   └── gan_summary/               # GAN SPI aggregated outputs
│   ├── SPI_comparison_all_windows.csv
│   └── MinMaxAvg.xlsx
│
└── requirements.txt
```

## Related Repositories

- [gpm-precipitation-downscaling](https://github.com/KGUHEC-hecshare21/gpm-precipitation-downscaling) - GAN/CNN/UNet downscaling models (upstream)
- [blrp-gamcheon-rainfall](https://github.com/KGUHEC-hecshare21/blrp-gamcheon-rainfall) - BLRP stochastic rainfall model

## Requirements

```bash
pip install -r requirements.txt
```

## License

MIT License
