# -*- coding: utf-8 -*-
"""
제주도 유역 지도 - 개선된 버전
- 4개 수역이 명확히 구분되는 색상
- 글씨 크기 확대
"""

import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 파일 경로 설정
# ============================================================
watershed_shapefile_path = r'/mnt/c/Yeonji/유역경계(grs80).shp'

# 출력 디렉토리 설정
output_dir = r'/mnt/c/Yeonji/2025.01.Drought/0.Manuscript/Figure'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# Shapefile 불러오기
# ============================================================
gdf = gpd.read_file(watershed_shapefile_path)

# 좌표계가 WGS84가 아니라면 변환
if gdf.crs.to_epsg() != 4326:
    gdf = gdf.to_crs(epsg=4326)

# 수역 이름 확인 (GUBUN 컬럼 기준)
regions = gdf['GUBUN'].unique().tolist()
print(f"발견된 수역: {regions}")

# ============================================================
# 수역별 색상 매핑 - 더 명확하게 구분되는 색상으로 변경
# ============================================================
region_colors = {
    '동부수역': '#E63946',  # 선명한 빨간색 (East)
    '서부수역': '#2A9D8F',  # 청록색/틸 (West)
    '남부수역': '#E9C46A',  # 노란색/골드 (South)
    '북부수역': '#264653'   # 진한 청색 (North)
}

# 한글 이름과 영어 이름 매핑
region_display_map = {
    '동부수역': 'East',
    '서부수역': 'West',
    '남부수역': 'South',
    '북부수역': 'North'
}

# ============================================================
# 그림 생성 - 크기 확대
# ============================================================
fig, ax = plt.subplots(figsize=(14, 12))

# 배경에 전체 제주도 윤곽 먼저 그리기 (회색으로)
gdf.boundary.plot(ax=ax, color='gray', linewidth=1.0)

# 각 수역별로 색상 채우기
for region_name, color in region_colors.items():
    region_gdf = gdf[gdf['GUBUN'] == region_name]
    if not region_gdf.empty:
        region_gdf.plot(ax=ax, color=color, edgecolor='black',
                        linewidth=2.0, alpha=0.85)

        # 수역 이름 레이블 추가 (중심에)
        centroid = region_gdf.geometry.centroid.iloc[0]
        display_name = region_display_map.get(region_name, region_name)
        ax.annotate(display_name,
                    xy=(centroid.x, centroid.y),
                    ha='center', va='center',
                    fontsize=20,  # 글씨 크기 크게
                    fontweight='bold',
                    color='white',
                    path_effects=[
                        path_effects.withStroke(linewidth=4, foreground='black')
                    ])

# 축 레이블 설정 - 글씨 크기 확대
ax.set_xlabel('Longitude (°E)', fontsize=18, fontweight='bold')
ax.set_ylabel('Latitude (°N)', fontsize=18, fontweight='bold')

# 축 눈금 글씨 크기 확대
ax.tick_params(axis='both', which='major', labelsize=16)

# 범례 생성 - 글씨 크기 확대
legend_patches = []
for region_name, color in region_colors.items():
    display_name = region_display_map.get(region_name, region_name)
    patch = mpatches.Patch(facecolor=color, edgecolor='black',
                           linewidth=2, label=display_name)
    legend_patches.append(patch)

legend = plt.legend(handles=legend_patches, loc='lower right',
                    fontsize=16, framealpha=0.95,
                    edgecolor='black', fancybox=False)
legend.get_frame().set_linewidth(2)

# 축 경계 자동 설정
plt.tight_layout()

# 축 눈금 설정 (보기 좋게)
plt.grid(True, linestyle='--', alpha=0.5, linewidth=1.0)

# 배경 지도 추가 (basemap) - 선택적
try:
    import contextily as ctx
    ctx.add_basemap(ax, crs=gdf.crs.to_string(),
                    source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.5)
    print("배경 지도가 성공적으로 추가되었습니다.")
except Exception as e:
    print(f"배경 지도 추가 실패: {e}")
    print("배경 지도 없이 계속합니다.")

# 방위표와 축적 제거됨 (사용자 요청)

# ============================================================
# 저장 및 표시
# ============================================================
output_path = os.path.join(output_dir, 'jeju_watersheds_map.png')
plt.savefig(output_path, dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"지도가 저장되었습니다: {output_path}")

# 추가: 수역별 정보 테이블 생성
watershed_area = {}
print("\n수역별 대략적인 면적 정보:")
print("=" * 50)
print(f"{'Watershed':<15} {'Area(km²)':<15}")
print("-" * 50)

for region_name in region_colors.keys():
    region_gdf = gdf[gdf['GUBUN'] == region_name]
    if not region_gdf.empty:
        # UTM zone 52N으로 변환하여 면적 계산 (미터 단위)
        region_utm = region_gdf.to_crs(epsg=32652)
        area_km2 = region_utm.geometry.area.sum() / 1e6
        display_name = region_display_map.get(region_name, region_name)
        watershed_area[display_name] = area_km2
        print(f"{display_name:<15} {area_km2:>10.2f}")

print("=" * 50)

plt.show()
print("\n완료!")
