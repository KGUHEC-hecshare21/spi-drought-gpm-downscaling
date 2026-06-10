# -*- coding: utf-8 -*-
"""
SPI 비교 그래프 - 개선된 버전
- 모든 글씨 크기 확대
- 더 명확한 시각화
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
output_dir = r'/mnt/c/Yeonji/2025.01.Drought/0.Manuscript/Figure/4.Results/3.Watershed'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# 데이터 설정
# 주의: 이 부분은 Analysis.ipynb에서 계산된 all_results를 사용해야 합니다.
# 아래는 예시 데이터입니다. 실제 사용시 Analysis.ipynb의 결과로 교체하세요.
# ============================================================

# 지역 정보
regions = ['동부수역', '북부수역', '서부수역', '남부수역']
regions_eng = ['East', 'North', 'West', 'South']

# 실제 데이터 (Analysis.ipynb에서 추출)
all_results = {
    'SPI3_GAN': {'동부수역': 0.2290, '북부수역': 0.2237, '서부수역': 0.2326, '남부수역': 0.2012},
    'SPI3_Cok': {'동부수역': 0.1845, '북부수역': 0.1817, '서부수역': 0.2056, '남부수역': 0.1942},
    'SPI6_GAN': {'동부수역': 0.2226, '북부수역': 0.2185, '서부수역': 0.2244, '남부수역': 0.1970},
    'SPI6_Cok': {'동부수역': 0.1871, '북부수역': 0.2064, '서부수역': 0.1939, '남부수역': 0.1886},
    'SPI9_GAN': {'동부수역': 0.2078, '북부수역': 0.1918, '서부수역': 0.1878, '남부수역': 0.1861},
    'SPI9_Cok': {'동부수역': 0.1737, '북부수역': 0.1742, '서부수역': 0.1949, '남부수역': 0.1819},
    'SPI12_GAN': {'동부수역': 0.1701, '북부수역': 0.1838, '서부수역': 0.1500, '남부수역': 0.1929},
    'SPI12_Cok': {'동부수역': 0.1866, '북부수역': 0.1767, '서부수역': 0.1800, '남부수역': 0.1898},
}

spi_periods = [3, 6, 9, 12]

# ============================================================
# 4.1) 개별 SPI 기간별 비교 그래프 (글씨 크기 확대)
# ============================================================
print("개별 SPI 비교 그래프 생성 중...")

for period in spi_periods:
    gan_key = f'SPI{period}_GAN'
    cok_key = f'SPI{period}_Cok'

    if gan_key in all_results or cok_key in all_results:
        # 그림 크기 확대
        fig, ax = plt.subplots(figsize=(12, 8))

        x = np.arange(len(regions))
        width = 0.35

        # GAN 데이터
        if gan_key in all_results:
            gan_values = [all_results[gan_key].get(r, np.nan) for r in regions]
            bars1 = ax.bar(x - width/2, gan_values, width, label='GAN',
                          color='steelblue', edgecolor='black', linewidth=1.5)

            # 값 레이블 추가 - 글씨 크기 확대
            for bar, value in zip(bars1, gan_values):
                if not np.isnan(value):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.008,
                           f'{value:.1%}', ha='center', va='bottom',
                           fontsize=14, fontweight='bold')

        # Cokriging 데이터
        if cok_key in all_results:
            cok_values = [all_results[cok_key].get(r, np.nan) for r in regions]
            bars2 = ax.bar(x + width/2, cok_values, width, label='Cokriging',
                          color='lightsteelblue', edgecolor='black', linewidth=1.5)

            # 값 레이블 추가 - 글씨 크기 확대
            for bar, value in zip(bars2, cok_values):
                if not np.isnan(value):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.008,
                           f'{value:.1%}', ha='center', va='bottom',
                           fontsize=14, fontweight='bold')

        # 축 레이블 - 글씨 크기 대폭 확대
        ax.set_xlabel('Watershed', fontsize=20, fontweight='bold')
        ax.set_ylabel('Averaged Drought Area (%)', fontsize=20, fontweight='bold')

        # X축 레이블 - 글씨 크기 확대
        ax.set_xticks(x)
        ax.set_xticklabels(regions_eng, rotation=0, fontsize=18, fontweight='bold')

        # Y축 눈금 글씨 크기 확대
        ax.tick_params(axis='y', labelsize=16)
        ax.tick_params(direction='in', length=6, width=1.5)

        # 범례 - 글씨 크기 확대
        legend = ax.legend(fontsize=16, loc='upper right',
                          framealpha=0.95, edgecolor='black')
        legend.get_frame().set_linewidth(1.5)

        # 그리드
        ax.grid(True, alpha=0.3, axis='y', linewidth=1.0)

        # Y축 범위 설정
        ax.set_ylim(0, 0.30)

        # 테두리 두께
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)

        plt.tight_layout()

        # 저장 (600 dpi)
        fig_path = os.path.join(output_dir, f'SPI{period}_comparison.png')
        fig.savefig(fig_path, dpi=600, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        print(f"저장 완료: {fig_path}")

        plt.close()

# ============================================================
# 4.2) 모든 SPI 기간 통합 비교 (2x2 서브플롯)
# ============================================================
print("\n통합 SPI 비교 그래프 생성 중...")

fig, axes = plt.subplots(2, 2, figsize=(20, 16))
axes = axes.ravel()

for idx, period in enumerate(spi_periods):
    ax = axes[idx]
    gan_key = f'SPI{period}_GAN'
    cok_key = f'SPI{period}_Cok'

    x = np.arange(len(regions))
    width = 0.35

    # GAN 데이터
    if gan_key in all_results:
        gan_values = [all_results[gan_key].get(r, np.nan) for r in regions]
        bars1 = ax.bar(x - width/2, gan_values, width, label='GAN',
                      color='steelblue', edgecolor='black', linewidth=1.5)

        for bar, value in zip(bars1, gan_values):
            if not np.isnan(value):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.008,
                       f'{value:.1%}', ha='center', va='bottom',
                       fontsize=12, fontweight='bold')

    # Cokriging 데이터
    if cok_key in all_results:
        cok_values = [all_results[cok_key].get(r, np.nan) for r in regions]
        bars2 = ax.bar(x + width/2, cok_values, width, label='Cokriging',
                      color='lightsteelblue', edgecolor='black', linewidth=1.5)

        for bar, value in zip(bars2, cok_values):
            if not np.isnan(value):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.008,
                       f'{value:.1%}', ha='center', va='bottom',
                       fontsize=12, fontweight='bold')

    # 서브플롯 제목 - 글씨 크기 확대
    ax.set_title(f'SPI-{period}', fontsize=22, fontweight='bold', pad=15)

    # 축 레이블 - 글씨 크기 확대
    ax.set_xlabel('Watershed', fontsize=18, fontweight='bold')
    ax.set_ylabel('Averaged Drought Area (%)', fontsize=18, fontweight='bold')

    # X축 레이블
    ax.set_xticks(x)
    ax.set_xticklabels(regions_eng, rotation=0, fontsize=16, fontweight='bold')

    # Y축 눈금
    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(direction='in', length=5, width=1.5)

    # 범례
    if idx == 0:  # 첫 번째 서브플롯에만 범례 표시
        legend = ax.legend(fontsize=14, loc='upper right',
                          framealpha=0.95, edgecolor='black')
        legend.get_frame().set_linewidth(1.5)

    # 그리드
    ax.grid(True, alpha=0.3, axis='y', linewidth=1.0)

    # Y축 범위
    ax.set_ylim(0, 0.30)

    # 테두리 두께
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

plt.tight_layout(pad=3.0)

# 저장
combined_fig_path = os.path.join(output_dir, 'all_SPI_comparison.png')
fig.savefig(combined_fig_path, dpi=600, bbox_inches='tight',
           facecolor='white', edgecolor='none')
print(f"저장 완료: {combined_fig_path}")

plt.close()

print("\n모든 그래프 생성 완료!")
print(f"출력 폴더: {output_dir}")
