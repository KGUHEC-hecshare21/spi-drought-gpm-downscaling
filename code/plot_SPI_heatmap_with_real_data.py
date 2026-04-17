# -*- coding: utf-8 -*-
"""
SPI Distribution Heatmap - 실제 데이터로 생성
- 실제 SPI 데이터에서 9개 카테고리별/5개 고도별 비율 계산
- 글씨 크기 대폭 확대
- X축 레이블에서 괄호 안 숫자 제거
"""

import os
import sys
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import rasterio
from scipy.ndimage import zoom
import warnings
warnings.filterwarnings('ignore')

# 출력 버퍼링 해제
sys.stdout.reconfigure(line_buffering=True)

# 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 경로 설정 (WSL 경로)
# ============================================================
base_folder = '/mnt/c/Yeonji/2025.01.Drought/2004'
dem_path = '/mnt/c/Yeonji/2025.01.Drought/DEM_Jeju.tif'
output_dir = '/mnt/c/Yeonji/2025.01.Drought/0.Manuscript/Figure/4.Results/4.Elevation'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# SPI 카테고리 정의 (9개)
# ============================================================
def get_spi_categories():
    return {
        'Extreme Drought (≤-2.0)': (-np.inf, -2.0),
        'Severe Drought (-2.0~-1.5)': (-2.0, -1.5),
        'Moderate Drought (-1.5~-1.0)': (-1.5, -1.0),
        'Slight Drought (-1.0~-0.5)': (-1.0, -0.5),
        'Normal (-0.5~0.5)': (-0.5, 0.5),
        'Slight Wet (0.5~1.0)': (0.5, 1.0),
        'Moderate Wet (1.0~1.5)': (1.0, 1.5),
        'Severe Wet (1.5~2.0)': (1.5, 2.0),
        'Extreme Wet (≥2.0)': (2.0, np.inf)
    }

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

# ============================================================
# DEM 로드 및 고도 마스크 생성
# ============================================================
def load_and_resize_dem(dem_path, target_shape):
    print(f"📍 Loading DEM from: {dem_path}")
    try:
        with rasterio.open(dem_path) as src:
            dem_original = src.read(1)
            zoom_y = target_shape[0] / dem_original.shape[0]
            zoom_x = target_shape[1] / dem_original.shape[1]
            dem_resized = zoom(dem_original, (zoom_y, zoom_x), order=1)
            print(f"✅ DEM resized from {dem_original.shape} to {dem_resized.shape}")
            return dem_resized
    except Exception as e:
        print(f"❌ Error loading DEM: {e}")
        return None

def create_elevation_masks(dem_array):
    print("🏔️ Creating elevation masks...")
    elevation_ranges = {
        '≤ 50m': (0, 50),
        '50-200m': (50, 200),
        '200-500m': (200, 500),
        '500-900m': (500, 900),
        '>900m': (900, np.inf)
    }
    masks = {}
    for range_name, (min_elev, max_elev) in elevation_ranges.items():
        mask = (dem_array >= min_elev) & (dem_array < max_elev)
        masks[range_name] = mask
        count = np.sum(mask)
        print(f"   {range_name}: {count} grid points")
    return masks

# ============================================================
# SPI 분석 함수
# ============================================================
def analyze_spi_by_categories_and_elevation(spi_period, data_type, elevation_masks):
    folder_map = {'GAN': 'SPI(GAN)', 'Cok': 'SPI(Cok)'}
    spi_folder = os.path.join(base_folder, folder_map[data_type], f'SPI{spi_period}({data_type})')

    print(f"\n=== Analyzing SPI{spi_period} ({data_type}) ===")
    if not os.path.exists(spi_folder):
        print(f"❌ Folder does not exist: {spi_folder}")
        return None

    spi_files = sorted(glob.glob(os.path.join(spi_folder, "*.nc")))
    if not spi_files:
        print(f"❌ No .nc files found in {spi_folder}")
        return None
    print(f"📁 Found {len(spi_files)} files")

    try:
        # Try loading with open_mfdataset
        spi = xr.open_mfdataset(
            spi_files,
            combine='nested',
            concat_dim='time',
            data_vars='all',
            coords='all',
            compat='override'
        )[f'SPI{spi_period}']
        print("✅ Successfully loaded with open_mfdataset")
    except Exception as e:
        print(f"⚠️ open_mfdataset failed: {e}. Trying alternative loading.")
        try:
            spi_list = []
            for f in spi_files:
                ds = xr.open_dataset(f)
                if f'SPI{spi_period}' in ds.data_vars:
                    spi_list.append(ds[f'SPI{spi_period}'])
                ds.close()
            spi = xr.concat(spi_list, dim='time')
            print("✅ Successfully loaded with alternative method")
        except Exception as e2:
            print(f"❌ Alternative loading also failed: {e2}")
            return None

    print(f"🔍 Data shape: {spi.shape}")

    results = {}
    spi_categories = get_spi_categories()

    for elev_range, elev_mask in elevation_masks.items():
        results[elev_range] = {}

        # Create mask DataArray with correct dimensions
        spatial_dims = [d for d in spi.dims if d != 'time']
        mask_da = xr.DataArray(elev_mask, dims=spatial_dims)

        spi_elevation = spi.where(mask_da)
        total_valid = spi_elevation.count().values

        if total_valid == 0:
            for category in spi_categories:
                results[elev_range][category] = 0.0
            continue

        for category, (min_val, max_val) in spi_categories.items():
            category_mask = (spi_elevation > min_val) & (spi_elevation <= max_val)
            category_count = category_mask.sum().values
            ratio = category_count / total_valid if total_valid > 0 else 0
            results[elev_range][category] = float(ratio)

    return results

# ============================================================
# 개선된 Heatmap 플롯 함수
# ============================================================
def plot_distribution_heatmap_enhanced(period, results_data, elev_ranges, spi_cats_orig, spi_cats_display, output_path):
    gan_key = f'SPI{period}_GAN'
    cok_key = f'SPI{period}_Cok'

    if not (gan_key in results_data and cok_key in results_data):
        print(f"⚠️ Data missing for SPI{period}. Skipping plot.")
        return

    # 데이터 준비
    gan_data = np.array([[results_data[gan_key][elev].get(cat, 0) for cat in spi_cats_orig] for elev in elev_ranges])
    cok_data = np.array([[results_data[cok_key][elev].get(cat, 0) for cat in spi_cats_orig] for elev in elev_ranges])
    v_max = max(gan_data.max(), cok_data.max()) * 1.05

    n_rows, n_cols = gan_data.shape

    # 그림 크기 설정 (컬러바 공간 포함)
    fig = plt.figure(figsize=(26, 10))

    # GridSpec으로 레이아웃 설정 (2개 플롯 + 컬러바)
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.15)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    cbar_ax = fig.add_subplot(gs[0, 2])

    datasets = [('GAN', gan_data, ax1), ('Cokriging', cok_data, ax2)]
    cmap = plt.cm.RdYlBu

    for title, data, ax in datasets:
        # pcolormesh 사용 (흰 선 방지)
        x = np.arange(n_cols + 1)
        y = np.arange(n_rows + 1)
        mesh = ax.pcolormesh(x, y, data, cmap=cmap, vmin=0, vmax=v_max,
                             edgecolors='face', linewidth=0, antialiased=False)

        # 셀 중앙에 텍스트 추가
        for i in range(n_rows):
            for j in range(n_cols):
                val = data[i, j]
                norm_val = val / v_max if v_max > 0 else 0
                text_color = "white" if norm_val > 0.6 or norm_val < 0.25 else "black"
                ax.text(j + 0.5, i + 0.5, f'{val:.1%}', ha='center', va='center',
                       fontsize=14, fontweight='bold', color=text_color)

        # 제목
        ax.set_title(title, fontsize=24, fontweight='bold', pad=15)

        # X축 설정
        ax.set_xticks(np.arange(n_cols) + 0.5)
        ax.set_xticklabels(spi_cats_display, fontsize=13, fontweight='bold', ha='center')

        # Y축 설정
        ax.set_yticks(np.arange(n_rows) + 0.5)
        if ax == ax1:
            ax.set_yticklabels(elev_ranges, fontsize=16, fontweight='bold')
        else:
            ax.set_yticklabels([])

        ax.set_xlim(0, n_cols)
        ax.set_ylim(0, n_rows)
        ax.invert_yaxis()  # Y축 뒤집기 (위에서 아래로)

        # 테두리
        for spine in ax.spines.values():
            spine.set_linewidth(2)

    # 컬러바 (별도 축에 배치)
    cbar = fig.colorbar(mesh, cax=cbar_ax)
    cbar.set_label('Ratio', fontsize=18, fontweight='bold')
    cbar.ax.tick_params(labelsize=14)

    # 저장
    fig.savefig(output_path, dpi=600, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"💾 Heatmap saved to: {output_path}")

# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("🎯 SPI Distribution Heatmap - 실제 데이터 분석 시작")
    print("=" * 70)

    # 테스트 파일에서 target shape 가져오기
    test_file_path = os.path.join(base_folder, 'SPI(GAN)/SPI3(GAN)/200403_SPI3.nc')

    if not os.path.exists(test_file_path):
        print(f"❌ Test SPI file not found at: {test_file_path}")
        exit()

    with xr.open_dataset(test_file_path) as test_ds:
        spi_var = [v for v in test_ds.data_vars if 'SPI' in v.upper()][0]
        target_shape = test_ds[spi_var].shape[-2:]
        print(f"📐 Target shape: {target_shape}")

    # DEM 로드
    if os.path.exists(dem_path):
        dem_array = load_and_resize_dem(dem_path, target_shape)
    else:
        print(f"⚠️ DEM file not found at {dem_path}, using random elevation data")
        dem_array = np.random.uniform(0, 1000, target_shape)

    if dem_array is None:
        print("❌ Failed to load DEM")
        exit()

    # 고도 마스크 생성
    elevation_masks = create_elevation_masks(dem_array)
    elevation_ranges_list = list(elevation_masks.keys())

    # SPI 분석 실행
    spi_periods = [3, 6, 9, 12]
    data_types = ['GAN', 'Cok']
    all_results = {}

    print("\n" + "=" * 70)
    print("📊 SPI 분석 시작...")
    print("=" * 70)

    for period in spi_periods:
        for data_type in data_types:
            results = analyze_spi_by_categories_and_elevation(period, data_type, elevation_masks)
            if results:
                all_results[f'SPI{period}_{data_type}'] = results
                print(f"✅ Successfully stored results for SPI{period}_{data_type}")
            else:
                print(f"❌ Failed to analyze SPI{period}_{data_type}")

    # 시각화
    print("\n" + "=" * 70)
    print("🎨 Heatmap 생성 중...")
    print("=" * 70)

    spi_categories_original = list(get_spi_categories().keys())

    for p in spi_periods:
        heatmap_fig_path = os.path.join(output_dir, f'SPI{p}_distribution_heatmap_revised.png')
        plot_distribution_heatmap_enhanced(
            p, all_results, elevation_ranges_list,
            spi_categories_original, spi_categories_display,
            heatmap_fig_path
        )

    print("\n" + "=" * 70)
    print("🎉 모든 작업 완료!")
    print(f"출력 폴더: {output_dir}")
    print("=" * 70)
