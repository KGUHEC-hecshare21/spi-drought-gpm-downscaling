# -*- coding: utf-8 -*-
"""
SPI Distribution Heatmap - 개선된 버전
- 글씨 크기 대폭 확대
- X축 레이블에서 괄호 안 숫자 제거
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 출력 디렉토리 설정
# ============================================================
output_dir = r'/mnt/c/Yeonji/2025.01.Drought/0.Manuscript/Figure/4.Results/4.Elevation'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# SPI 카테고리 정의 (괄호 안 숫자 제거된 버전)
# ============================================================
# 원본 카테고리 (데이터 키로 사용)
spi_categories_original = [
    'Extreme Drought (≤-2.0)',
    'Severe Drought (-2.0~-1.5)',
    'Moderate Drought (-1.5~-1.0)',
    'Slight Drought (-1.0~-0.5)',
    'Normal (-0.5~0.5)',
    'Slight Wet (0.5~1.0)',
    'Moderate Wet (1.0~1.5)',
    'Severe Wet (1.5~2.0)',
    'Extreme Wet (≥2.0)'
]

# X축에 표시할 레이블 (괄호 제거)
spi_categories_display = [
    'Extreme\nDrought',
    'Severe\nDrought',
    'Moderate\nDrought',
    'Slight\nDrought',
    'Normal',
    'Slight\nWet',
    'Moderate\nWet',
    'Severe\nWet',
    'Extreme\nWet'
]

# 고도 범위
elevation_ranges = ['≤ 50m', '50-200m', '200-500m', '500-900m', '>900m']

# ============================================================
# 예시 데이터 (실제 데이터로 교체 필요)
# 구조: all_results[f'SPI{period}_{type}'][elevation][category] = ratio
# ============================================================
# 아래는 SPI.ipynb에서 계산된 all_results 구조의 예시입니다.
# 실제 사용 시 SPI.ipynb의 all_results 데이터를 복사해서 사용하세요.

all_results = {
    'SPI3_GAN': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.000, 'Severe Drought (-2.0~-1.5)': 0.032, 'Moderate Drought (-1.5~-1.0)': 0.152, 'Slight Drought (-1.0~-0.5)': 0.180, 'Normal (-0.5~0.5)': 0.350, 'Slight Wet (0.5~1.0)': 0.140, 'Moderate Wet (1.0~1.5)': 0.085, 'Severe Wet (1.5~2.0)': 0.056, 'Extreme Wet (≥2.0)': 0.031},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.000, 'Severe Drought (-2.0~-1.5)': 0.033, 'Moderate Drought (-1.5~-1.0)': 0.148, 'Slight Drought (-1.0~-0.5)': 0.175, 'Normal (-0.5~0.5)': 0.355, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.085, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.030},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.000, 'Severe Drought (-2.0~-1.5)': 0.036, 'Moderate Drought (-1.5~-1.0)': 0.142, 'Slight Drought (-1.0~-0.5)': 0.170, 'Normal (-0.5~0.5)': 0.360, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.079, 'Severe Wet (1.5~2.0)': 0.065, 'Extreme Wet (≥2.0)': 0.028},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.000, 'Severe Drought (-2.0~-1.5)': 0.036, 'Moderate Drought (-1.5~-1.0)': 0.142, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.362, 'Slight Wet (0.5~1.0)': 0.140, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.065, 'Extreme Wet (≥2.0)': 0.028},
        '>900m': {'Extreme Drought (≤-2.0)': 0.000, 'Severe Drought (-2.0~-1.5)': 0.034, 'Moderate Drought (-1.5~-1.0)': 0.142, 'Slight Drought (-1.0~-0.5)': 0.165, 'Normal (-0.5~0.5)': 0.368, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.075, 'Severe Wet (1.5~2.0)': 0.070, 'Extreme Wet (≥2.0)': 0.024},
    },
    'SPI3_Cok': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.005, 'Severe Drought (-2.0~-1.5)': 0.034, 'Moderate Drought (-1.5~-1.0)': 0.153, 'Slight Drought (-1.0~-0.5)': 0.178, 'Normal (-0.5~0.5)': 0.345, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.086, 'Severe Wet (1.5~2.0)': 0.053, 'Extreme Wet (≥2.0)': 0.028},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.002, 'Severe Drought (-2.0~-1.5)': 0.035, 'Moderate Drought (-1.5~-1.0)': 0.154, 'Slight Drought (-1.0~-0.5)': 0.176, 'Normal (-0.5~0.5)': 0.348, 'Slight Wet (0.5~1.0)': 0.140, 'Moderate Wet (1.0~1.5)': 0.084, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.029},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.001, 'Severe Drought (-2.0~-1.5)': 0.031, 'Moderate Drought (-1.5~-1.0)': 0.147, 'Slight Drought (-1.0~-0.5)': 0.172, 'Normal (-0.5~0.5)': 0.355, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.030},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.001, 'Severe Drought (-2.0~-1.5)': 0.031, 'Moderate Drought (-1.5~-1.0)': 0.147, 'Slight Drought (-1.0~-0.5)': 0.170, 'Normal (-0.5~0.5)': 0.358, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.060, 'Extreme Wet (≥2.0)': 0.028},
        '>900m': {'Extreme Drought (≤-2.0)': 0.001, 'Severe Drought (-2.0~-1.5)': 0.028, 'Moderate Drought (-1.5~-1.0)': 0.144, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.362, 'Slight Wet (0.5~1.0)': 0.145, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.062, 'Extreme Wet (≥2.0)': 0.026},
    },
    'SPI6_GAN': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.004, 'Severe Drought (-2.0~-1.5)': 0.047, 'Moderate Drought (-1.5~-1.0)': 0.133, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.358, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.085, 'Severe Wet (1.5~2.0)': 0.052, 'Extreme Wet (≥2.0)': 0.028},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.004, 'Severe Drought (-2.0~-1.5)': 0.048, 'Moderate Drought (-1.5~-1.0)': 0.134, 'Slight Drought (-1.0~-0.5)': 0.170, 'Normal (-0.5~0.5)': 0.355, 'Slight Wet (0.5~1.0)': 0.140, 'Moderate Wet (1.0~1.5)': 0.086, 'Severe Wet (1.5~2.0)': 0.054, 'Extreme Wet (≥2.0)': 0.029},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.006, 'Severe Drought (-2.0~-1.5)': 0.047, 'Moderate Drought (-1.5~-1.0)': 0.137, 'Slight Drought (-1.0~-0.5)': 0.172, 'Normal (-0.5~0.5)': 0.352, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.084, 'Severe Wet (1.5~2.0)': 0.056, 'Extreme Wet (≥2.0)': 0.030},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.006, 'Severe Drought (-2.0~-1.5)': 0.049, 'Moderate Drought (-1.5~-1.0)': 0.138, 'Slight Drought (-1.0~-0.5)': 0.175, 'Normal (-0.5~0.5)': 0.348, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.032},
        '>900m': {'Extreme Drought (≤-2.0)': 0.006, 'Severe Drought (-2.0~-1.5)': 0.049, 'Moderate Drought (-1.5~-1.0)': 0.133, 'Slight Drought (-1.0~-0.5)': 0.178, 'Normal (-0.5~0.5)': 0.345, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.060, 'Extreme Wet (≥2.0)': 0.030},
    },
    'SPI6_Cok': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.009, 'Severe Drought (-2.0~-1.5)': 0.042, 'Moderate Drought (-1.5~-1.0)': 0.150, 'Slight Drought (-1.0~-0.5)': 0.172, 'Normal (-0.5~0.5)': 0.340, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.088, 'Severe Wet (1.5~2.0)': 0.050, 'Extreme Wet (≥2.0)': 0.030},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.006, 'Severe Drought (-2.0~-1.5)': 0.049, 'Moderate Drought (-1.5~-1.0)': 0.138, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.352, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.085, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.004, 'Severe Drought (-2.0~-1.5)': 0.048, 'Moderate Drought (-1.5~-1.0)': 0.135, 'Slight Drought (-1.0~-0.5)': 0.165, 'Normal (-0.5~0.5)': 0.358, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.028},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.004, 'Severe Drought (-2.0~-1.5)': 0.045, 'Moderate Drought (-1.5~-1.0)': 0.132, 'Slight Drought (-1.0~-0.5)': 0.162, 'Normal (-0.5~0.5)': 0.365, 'Slight Wet (0.5~1.0)': 0.145, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.026},
        '>900m': {'Extreme Drought (≤-2.0)': 0.004, 'Severe Drought (-2.0~-1.5)': 0.045, 'Moderate Drought (-1.5~-1.0)': 0.128, 'Slight Drought (-1.0~-0.5)': 0.160, 'Normal (-0.5~0.5)': 0.370, 'Slight Wet (0.5~1.0)': 0.148, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
    },
    'SPI9_GAN': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.015, 'Severe Drought (-2.0~-1.5)': 0.039, 'Moderate Drought (-1.5~-1.0)': 0.160, 'Slight Drought (-1.0~-0.5)': 0.175, 'Normal (-0.5~0.5)': 0.330, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.052, 'Extreme Wet (≥2.0)': 0.028},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.013, 'Severe Drought (-2.0~-1.5)': 0.048, 'Moderate Drought (-1.5~-1.0)': 0.147, 'Slight Drought (-1.0~-0.5)': 0.172, 'Normal (-0.5~0.5)': 0.340, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.053, 'Extreme Wet (≥2.0)': 0.027},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.013, 'Severe Drought (-2.0~-1.5)': 0.050, 'Moderate Drought (-1.5~-1.0)': 0.145, 'Slight Drought (-1.0~-0.5)': 0.170, 'Normal (-0.5~0.5)': 0.342, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.013, 'Severe Drought (-2.0~-1.5)': 0.050, 'Moderate Drought (-1.5~-1.0)': 0.145, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.345, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.028},
        '>900m': {'Extreme Drought (≤-2.0)': 0.016, 'Severe Drought (-2.0~-1.5)': 0.037, 'Moderate Drought (-1.5~-1.0)': 0.151, 'Slight Drought (-1.0~-0.5)': 0.165, 'Normal (-0.5~0.5)': 0.350, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.075, 'Severe Wet (1.5~2.0)': 0.058, 'Extreme Wet (≥2.0)': 0.026},
    },
    'SPI9_Cok': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.019, 'Severe Drought (-2.0~-1.5)': 0.070, 'Moderate Drought (-1.5~-1.0)': 0.134, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.335, 'Slight Wet (0.5~1.0)': 0.132, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.050, 'Extreme Wet (≥2.0)': 0.028},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.017, 'Severe Drought (-2.0~-1.5)': 0.067, 'Moderate Drought (-1.5~-1.0)': 0.114, 'Slight Drought (-1.0~-0.5)': 0.165, 'Normal (-0.5~0.5)': 0.350, 'Slight Wet (0.5~1.0)': 0.138, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.014, 'Severe Drought (-2.0~-1.5)': 0.064, 'Moderate Drought (-1.5~-1.0)': 0.103, 'Slight Drought (-1.0~-0.5)': 0.160, 'Normal (-0.5~0.5)': 0.365, 'Slight Wet (0.5~1.0)': 0.145, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.013, 'Severe Drought (-2.0~-1.5)': 0.062, 'Moderate Drought (-1.5~-1.0)': 0.103, 'Slight Drought (-1.0~-0.5)': 0.158, 'Normal (-0.5~0.5)': 0.368, 'Slight Wet (0.5~1.0)': 0.148, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.056, 'Extreme Wet (≥2.0)': 0.028},
        '>900m': {'Extreme Drought (≤-2.0)': 0.013, 'Severe Drought (-2.0~-1.5)': 0.056, 'Moderate Drought (-1.5~-1.0)': 0.112, 'Slight Drought (-1.0~-0.5)': 0.155, 'Normal (-0.5~0.5)': 0.372, 'Slight Wet (0.5~1.0)': 0.148, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
    },
    'SPI12_GAN': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.024, 'Severe Drought (-2.0~-1.5)': 0.087, 'Moderate Drought (-1.5~-1.0)': 0.070, 'Slight Drought (-1.0~-0.5)': 0.165, 'Normal (-0.5~0.5)': 0.365, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.052, 'Extreme Wet (≥2.0)': 0.028},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.031, 'Severe Drought (-2.0~-1.5)': 0.075, 'Moderate Drought (-1.5~-1.0)': 0.071, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.362, 'Slight Wet (0.5~1.0)': 0.140, 'Moderate Wet (1.0~1.5)': 0.085, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.032, 'Severe Drought (-2.0~-1.5)': 0.080, 'Moderate Drought (-1.5~-1.0)': 0.062, 'Slight Drought (-1.0~-0.5)': 0.162, 'Normal (-0.5~0.5)': 0.368, 'Slight Wet (0.5~1.0)': 0.145, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.032, 'Severe Drought (-2.0~-1.5)': 0.080, 'Moderate Drought (-1.5~-1.0)': 0.062, 'Slight Drought (-1.0~-0.5)': 0.160, 'Normal (-0.5~0.5)': 0.370, 'Slight Wet (0.5~1.0)': 0.148, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '>900m': {'Extreme Drought (≤-2.0)': 0.023, 'Severe Drought (-2.0~-1.5)': 0.102, 'Moderate Drought (-1.5~-1.0)': 0.052, 'Slight Drought (-1.0~-0.5)': 0.155, 'Normal (-0.5~0.5)': 0.375, 'Slight Wet (0.5~1.0)': 0.150, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.053, 'Extreme Wet (≥2.0)': 0.028},
    },
    'SPI12_Cok': {
        '≤ 50m': {'Extreme Drought (≤-2.0)': 0.018, 'Severe Drought (-2.0~-1.5)': 0.103, 'Moderate Drought (-1.5~-1.0)': 0.137, 'Slight Drought (-1.0~-0.5)': 0.168, 'Normal (-0.5~0.5)': 0.302, 'Slight Wet (0.5~1.0)': 0.128, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.052, 'Extreme Wet (≥2.0)': 0.028},
        '50-200m': {'Extreme Drought (≤-2.0)': 0.023, 'Severe Drought (-2.0~-1.5)': 0.073, 'Moderate Drought (-1.5~-1.0)': 0.136, 'Slight Drought (-1.0~-0.5)': 0.165, 'Normal (-0.5~0.5)': 0.320, 'Slight Wet (0.5~1.0)': 0.135, 'Moderate Wet (1.0~1.5)': 0.082, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '200-500m': {'Extreme Drought (≤-2.0)': 0.027, 'Severe Drought (-2.0~-1.5)': 0.061, 'Moderate Drought (-1.5~-1.0)': 0.125, 'Slight Drought (-1.0~-0.5)': 0.158, 'Normal (-0.5~0.5)': 0.340, 'Slight Wet (0.5~1.0)': 0.142, 'Moderate Wet (1.0~1.5)': 0.080, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '500-900m': {'Extreme Drought (≤-2.0)': 0.027, 'Severe Drought (-2.0~-1.5)': 0.061, 'Moderate Drought (-1.5~-1.0)': 0.125, 'Slight Drought (-1.0~-0.5)': 0.155, 'Normal (-0.5~0.5)': 0.345, 'Slight Wet (0.5~1.0)': 0.145, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
        '>900m': {'Extreme Drought (≤-2.0)': 0.029, 'Severe Drought (-2.0~-1.5)': 0.059, 'Moderate Drought (-1.5~-1.0)': 0.102, 'Slight Drought (-1.0~-0.5)': 0.148, 'Normal (-0.5~0.5)': 0.365, 'Slight Wet (0.5~1.0)': 0.152, 'Moderate Wet (1.0~1.5)': 0.078, 'Severe Wet (1.5~2.0)': 0.055, 'Extreme Wet (≥2.0)': 0.028},
    },
}

spi_periods = [3, 6, 9, 12]

# ============================================================
# 개선된 Heatmap 플롯 함수
# ============================================================
def plot_distribution_heatmap_enhanced(period, results_data, elev_ranges, spi_cats_orig, spi_cats_display, output_path):
    """
    개선된 SPI Distribution Heatmap
    - 글씨 크기 대폭 확대
    - X축 레이블에서 괄호 안 숫자 제거
    """
    gan_key = f'SPI{period}_GAN'
    cok_key = f'SPI{period}_Cok'

    if not (gan_key in results_data and cok_key in results_data):
        print(f"⚠️ Data missing for SPI{period}. Skipping plot.")
        return

    # 데이터 준비
    gan_data = np.array([[results_data[gan_key][elev].get(cat, 0) for cat in spi_cats_orig] for elev in elev_ranges])
    cok_data = np.array([[results_data[cok_key][elev].get(cat, 0) for cat in spi_cats_orig] for elev in elev_ranges])
    v_max = max(gan_data.max(), cok_data.max()) * 1.05

    # 그림 크기 확대
    fig, axes = plt.subplots(1, 2, figsize=(22, 9), sharey=True, constrained_layout=True)
    datasets = {'GAN': gan_data, 'Cokriging': cok_data}

    for ax, (title, data) in zip(axes, datasets.items()):
        im = ax.imshow(data, cmap='RdYlBu', aspect='auto', vmin=0, vmax=v_max)

        # 제목 - 글씨 크기 확대
        ax.set_title(title, fontsize=22, fontweight='bold', pad=15)

        # X축 레이블 - 괄호 제거된 버전 사용, 글씨 크기 확대
        ax.set_xticks(np.arange(len(spi_cats_display)))
        ax.set_xticklabels(spi_cats_display, rotation=0, ha='center', fontsize=14, fontweight='bold')

        # Y축 레이블 - 글씨 크기 확대
        ax.set_yticks(np.arange(len(elev_ranges)))
        ax.set_yticklabels(elev_ranges, fontsize=16, fontweight='bold')

        # 셀 안의 텍스트 - 글씨 크기 확대
        for i in range(len(elev_ranges)):
            for j in range(len(spi_cats_orig)):
                val = data[i, j]
                norm_val = (val - 0) / (v_max - 0) if v_max > 0 else 0
                text_color = "white" if norm_val > 0.65 or norm_val < 0.25 else "black"
                ax.text(j, i, f'{val:.1%}', ha="center", va="center",
                       color=text_color, fontsize=14, fontweight='bold')

        # 테두리 두께
        for spine in ax.spines.values():
            spine.set_linewidth(2)

    # 컬러바 - 글씨 크기 확대
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.8, pad=0.02)
    cbar.set_label('Ratio', fontsize=18, fontweight='bold')
    cbar.ax.tick_params(labelsize=14)

    # 저장
    fig.savefig(output_path, dpi=600, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"💾 Heatmap saved to: {output_path}")

# ============================================================
# 실행
# ============================================================
print("=" * 60)
print("🎨 Creating Enhanced SPI Distribution Heatmaps...")
print("=" * 60)

for p in spi_periods:
    heatmap_fig_path = os.path.join(output_dir, f'SPI{p}_distribution_heatmap_revised.png')
    plot_distribution_heatmap_enhanced(
        p, all_results, elevation_ranges,
        spi_categories_original, spi_categories_display,
        heatmap_fig_path
    )

print("\n🎉 모든 Heatmap 생성 완료!")
print(f"출력 폴더: {output_dir}")
