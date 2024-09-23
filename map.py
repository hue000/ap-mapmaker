import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from shapely.geometry import Point, MultiPolygon, LineString
from shapely.prepared import prep
from rtree import index
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


# 1. 创建网格点
# 2. 将网格点按经度分割成指定数量的部分
# 3. 将几何体按经度分割成指定数量的部分
# 4. 将点按经度分割成指定数量的部分
# 5. 处理点
# 6. 绘制地图
# 7. 保存地图
# 8. 显示地图

def create_grid_points(lands, borders, num_parts=8, resolution=2):
    """创建经纬度网格点"""
    land_points = []
    part = int(360/num_parts)
    
    for land in lands:
        lons = np.arange(land.bounds[0], land.bounds[2], resolution)
        lats = np.arange(land.bounds[1], land.bounds[3], resolution)
       
        for lon in lons:
            for lat in lats:
                if land.contains(Point(lon, lat)):
                    land_points.append((lon, lat))
        
    return land_points


def map():
    start_time = time.time()
    print(f"开始绘制地图:{start_time:.2f}")   

    fig = plt.figure(figsize=(30, 15))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.axis('off')
    ax.set_extent([-180, 180, -60, 90])
    ax.add_feature(cfeature.BORDERS, edgecolor='gray', linewidth=1,linestyle=':', alpha=0.5)

    lands = list(cfeature.LAND.geometries())
    borders = list(cfeature.BORDERS.geometries())
    land_points = create_grid_points(lands, borders, 8, 0.4)

    if land_points:
        xs_land, ys_land = zip(*land_points)
        ax.scatter(xs_land, ys_land, transform=ccrs.PlateCarree(), color='skyblue', s=1.2, alpha=0.5)
    else:
        print("没有找到陆地点")
    
    svg_path = 'world_map_dotted.png'
    plt.savefig(svg_path, format='png', dpi=400, bbox_inches=None,pad_inches=0)
    plt.show()
    return ax



if __name__ == '__main__':
    ax = map()
 

