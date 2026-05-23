import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.CheckinSpot import CheckinSpot

def update_all_spots_coords():
    with app.app_context():
        print("更新所有打卡点经纬度...")
        
        spots_updates = [
            {'name': '黄鹤楼', 'latitude': 30.5444, 'longitude': 114.2980},
            {'name': '东湖绿道', 'latitude': 30.5588, 'longitude': 114.3684},
            {'name': '湖北省博物馆', 'latitude': 30.5635, 'longitude': 114.3621},
            {'name': '楚河汉街', 'latitude': 30.5562, 'longitude': 114.3328},
            {'name': '昙华林', 'latitude': 30.5455, 'longitude': 114.3063},
            {'name': '武汉工程大学', 'latitude': 30.4820, 'longitude': 114.4221},
            {'name': '星巴克臻选(武汉天地店)', 'latitude': 30.6103, 'longitude': 114.3089},
            {'name': '西西弗书店(凯德广场店)', 'latitude': 30.5741, 'longitude': 114.2645},
            {'name': '武汉长江大桥', 'latitude': 30.5496, 'longitude': 114.2886},
            {'name': '户部巷', 'latitude': 30.5437, 'longitude': 114.2968},
            {'name': '汉口江滩', 'latitude': 30.5945, 'longitude': 114.3025},
            {'name': '武汉大学', 'latitude': 30.5416, 'longitude': 114.3663},
            {'name': '湖北省美术馆', 'latitude': 30.5619, 'longitude': 114.3598},
            {'name': '武汉植物园', 'latitude': 30.5429, 'longitude': 114.4121},
            {'name': '光谷广场', 'latitude': 30.5060, 'longitude': 114.4104},
            {'name': '知音号', 'latitude': 30.5992, 'longitude': 114.3067},
            {'name': '武汉科技馆', 'latitude': 30.5819, 'longitude': 114.2986},
            {'name': '汉正街', 'latitude': 30.5710, 'longitude': 114.2796},
            {'name': '湖北美术馆', 'latitude': 30.5436, 'longitude': 114.2962},
            {'name': 'Manner Coffee(武汉恒隆店)', 'latitude': 30.5794, 'longitude': 114.2731},
            {'name': '武汉东湖磨山景区', 'latitude': 30.5519, 'longitude': 114.4063},
            {'name': '新华书店(江汉路店)', 'latitude': 30.5797, 'longitude': 114.2860},
            {'name': '武汉欢乐谷', 'latitude': 30.5876, 'longitude': 114.3978},
            {'name': '江汉关博物馆', 'latitude': 30.5778, 'longitude': 114.2962},
            {'name': 'Today便利店(花园道店)', 'latitude': 30.5914, 'longitude': 114.2647},
            {'name': '武汉长江二桥', 'latitude': 30.6144, 'longitude': 114.3242},
            {'name': '万林艺术博物馆', 'latitude': 30.5419, 'longitude': 114.3658},
            {'name': '东湖樱花园', 'latitude': 30.5512, 'longitude': 114.4086}
        ]
        
        updated_count = 0
        not_found_count = 0
        for spot_update in spots_updates:
            spot = CheckinSpot.query.filter_by(name=spot_update['name']).first()
            if spot:
                spot.latitude = spot_update['latitude']
                spot.longitude = spot_update['longitude']
                updated_count += 1
                print(f"已更新: {spot_update['name']}")
            else:
                not_found_count += 1
                print(f"未找到: {spot_update['name']}")
        
        db.session.commit()
        print(f"\n更新完成！成功更新 {updated_count} 个打卡点，{not_found_count} 个未找到")

if __name__ == '__main__':
    update_all_spots_coords()
