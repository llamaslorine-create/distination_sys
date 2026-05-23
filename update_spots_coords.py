import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.CheckinSpot import CheckinSpot

def update_spots_coords():
    with app.app_context():
        print("更新打卡点经纬度...")
        
        spots_updates = [
            {
                'name': '武汉长江大桥',
                'latitude': 30.55232,
                'longitude': 114.28257
            },
            {
                'name': '户部巷',
                'latitude': 30.54686,
                'longitude': 114.29745
            },
            {
                'name': '汉口江滩',
                'latitude': 30.5832,
                'longitude': 114.30034
            },
            {
                'name': '武汉大学',
                'latitude': 30.534756,
                'longitude': 114.369011
            },
            {
                'name': '湖北省美术馆',
                'latitude': 30.566585,
                'longitude': 114.359546
            },
            {
                'name': '武汉植物园',
                'latitude': 30.54442,
                'longitude': 114.4234
            },
            {
                'name': '光谷广场',
                'latitude': 30.511968,
                'longitude': 114.405651
            },
            {
                'name': '知音号',
                'latitude': 30.585,
                'longitude': 114.295
            },
            {
                'name': '武汉科技馆',
                'latitude': 30.5901,
                'longitude': 114.2902
            },
            {
                'name': '汉正街',
                'latitude': 30.577378,
                'longitude': 114.281734
            },
            {
                'name': '湖北美术馆',
                'latitude': 30.566585,
                'longitude': 114.359546
            },
            {
                'name': 'Manner Coffee(武汉恒隆店)',
                'latitude': 30.577836,
                'longitude': 114.273801
            },
            {
                'name': '武汉东湖磨山景区',
                'latitude': 30.55123,
                'longitude': 114.41276
            },
            {
                'name': '新华书店(江汉路店)',
                'latitude': 30.580646,
                'longitude': 114.289381
            },
            {
                'name': '武汉欢乐谷',
                'latitude': 30.591334,
                'longitude': 114.392846
            },
            {
                'name': '江汉关博物馆',
                'latitude': 30.580646,
                'longitude': 114.298882
            },
            {
                'name': 'Today便利店(花园道店)',
                'latitude': 30.595902,
                'longitude': 114.350659
            },
            {
                'name': '武汉长江二桥',
                'latitude': 30.58016,
                'longitude': 114.3008
            },
            {
                'name': '万林艺术博物馆',
                'latitude': 30.5405,
                'longitude': 114.3665
            },
            {
                'name': '东湖樱花园',
                'latitude': 30.5505,
                'longitude': 114.3855
            }
        ]
        
        updated_count = 0
        for spot_update in spots_updates:
            spot = CheckinSpot.query.filter_by(name=spot_update['name']).first()
            if spot:
                spot.latitude = spot_update['latitude']
                spot.longitude = spot_update['longitude']
                updated_count += 1
                print(f"已更新: {spot_update['name']}")
        
        db.session.commit()
        print(f"成功更新 {updated_count} 个打卡点的经纬度！")

if __name__ == '__main__':
    update_spots_coords()
