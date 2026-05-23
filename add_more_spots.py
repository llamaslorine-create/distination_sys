import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.CheckinSpot import CheckinSpot

def add_more_spots():
    with app.app_context():
        print("添加更多打卡点...")
        
        more_spots = [
            {
                'name': '武汉长江大桥',
                'address': '武汉市武昌区临江大道与龟山南路交汇处',
                'latitude': 30.55232,
                'longitude': 114.28257,
                'category': '小众景点',
                'description': '长江上第一座铁路公路两用桥',
                'rating': 4.7,
                'checkin_count': 21560,
                'status': 1
            },
            {
                'name': '户部巷',
                'address': '武汉市武昌区自由路',
                'latitude': 30.54686,
                'longitude': 114.29745,
                'category': '餐厅',
                'description': '百年小吃街，武汉美食聚集地',
                'rating': 4.3,
                'checkin_count': 32580,
                'status': 1
            },
            {
                'name': '汉口江滩',
                'address': '武汉市江岸区沿江大道',
                'latitude': 30.5832,
                'longitude': 114.30034,
                'category': '小众景点',
                'description': '长江边最美的城市江滩公园',
                'rating': 4.6,
                'checkin_count': 17890,
                'status': 1
            },
            {
                'name': '武汉大学',
                'address': '武汉市武昌区珞喻路129号',
                'latitude': 30.534756,
                'longitude': 114.369011,
                'category': '小众景点',
                'description': '中国最美大学之一，樱花季必打卡',
                'rating': 4.8,
                'checkin_count': 35670,
                'status': 1
            },
            {
                'name': '湖北省美术馆',
                'address': '武汉市武昌区东湖路三官殿1号',
                'latitude': 30.566585,
                'longitude': 114.359546,
                'category': '美术馆',
                'description': '省级美术馆，展览湖北当代艺术',
                'rating': 4.4,
                'checkin_count': 5670,
                'status': 1
            },
            {
                'name': '武汉植物园',
                'address': '武汉市洪山区鲁磨路特1号',
                'latitude': 30.54442,
                'longitude': 114.4234,
                'category': '小众景点',
                'description': '中国三大植物园之一，四季花开',
                'rating': 4.5,
                'checkin_count': 11890,
                'status': 1
            },
            {
                'name': '光谷广场',
                'address': '武汉市洪山区珞喻路光谷广场',
                'latitude': 30.511968,
                'longitude': 114.405651,
                'category': '文创店',
                'description': '武汉地标性商圈，购物休闲一体化',
                'rating': 4.4,
                'checkin_count': 25780,
                'status': 1
            },
            {
                'name': '知音号',
                'address': '武汉市江岸区沿江大道江滩公园知音号码头',
                'latitude': 30.585,
                'longitude': 114.295,
                'category': '小众景点',
                'description': '漂移式多维体验剧，沉浸民国风情',
                'rating': 4.7,
                'checkin_count': 8920,
                'status': 1
            },
            {
                'name': '武汉科技馆',
                'address': '武汉市江岸区沿江大道91号',
                'latitude': 30.5901,
                'longitude': 114.2902,
                'category': '小众景点',
                'description': '现代科技展览，亲子游好去处',
                'rating': 4.6,
                'checkin_count': 13560,
                'status': 1
            },
            {
                'name': '汉正街',
                'address': '武汉市硚口区汉正街',
                'latitude': 30.577378,
                'longitude': 114.281734,
                'category': '文创店',
                'description': '天下第一街，小商品批发集散地',
                'rating': 4.2,
                'checkin_count': 18970,
                'status': 1
            },
            {
                'name': '湖北美术馆',
                'address': '武汉市武昌区中山路368号',
                'latitude': 30.566585,
                'longitude': 114.359546,
                'category': '美术馆',
                'description': '专业美术馆，展示湖北艺术精品',
                'rating': 4.5,
                'checkin_count': 6780,
                'status': 1
            },
            {
                'name': 'Manner Coffee(武汉恒隆店)',
                'address': '武汉市硚口区京汉大道668号武汉恒隆广场',
                'latitude': 30.577836,
                'longitude': 114.273801,
                'category': '咖啡馆',
                'description': '精品咖啡馆，高性价比好咖啡',
                'rating': 4.7,
                'checkin_count': 4560,
                'status': 1
            },
            {
                'name': '武汉东湖磨山景区',
                'address': '武汉市武昌区东湖生态旅游风景区磨山',
                'latitude': 30.55123,
                'longitude': 114.41276,
                'category': '小众景点',
                'description': '楚文化旅游区，四季皆有美景',
                'rating': 4.6,
                'checkin_count': 14230,
                'status': 1
            },
            {
                'name': '新华书店(江汉路店)',
                'address': '武汉市江汉区江汉路257号',
                'latitude': 30.580646,
                'longitude': 114.289381,
                'category': '书店',
                'description': '百年老字号，书香氛围浓厚',
                'rating': 4.4,
                'checkin_count': 3230,
                'status': 1
            },
            {
                'name': '武汉欢乐谷',
                'address': '武汉市洪山区东湖生态旅游风景区欢乐大道196号',
                'latitude': 30.591334,
                'longitude': 114.392846,
                'category': '小众景点',
                'description': '华中主题乐园，刺激欢乐并存',
                'rating': 4.5,
                'checkin_count': 18790,
                'status': 1
            },
            {
                'name': '江汉关博物馆',
                'address': '武汉市江岸区沿江大道129号',
                'latitude': 30.580646,
                'longitude': 114.298882,
                'category': '小众景点',
                'description': '武汉地标建筑，见证城市历史变迁',
                'rating': 4.7,
                'checkin_count': 9870,
                'status': 1
            },
            {
                'name': 'Today便利店(花园道店)',
                'address': '武汉市江汉区青年路308号花园道',
                'latitude': 30.595902,
                'longitude': 114.350659,
                'category': '餐厅',
                'description': '武汉本土便利店，网红美食聚集地',
                'rating': 4.5,
                'checkin_count': 6540,
                'status': 1
            },
            {
                'name': '武汉长江二桥',
                'address': '武汉市江岸区沿江大道',
                'latitude': 30.58016,
                'longitude': 114.3008,
                'category': '小众景点',
                'description': '长江上第二座大桥，夜景迷人',
                'rating': 4.4,
                'checkin_count': 11230,
                'status': 1
            },
            {
                'name': '万林艺术博物馆',
                'address': '武汉市武昌区珞喻路129号武汉大学内',
                'latitude': 30.5405,
                'longitude': 114.3665,
                'category': '美术馆',
                'description': '大学校园里的现代艺术博物馆',
                'rating': 4.6,
                'checkin_count': 5430,
                'status': 1
            },
            {
                'name': '东湖樱花园',
                'address': '武汉市武昌区东湖生态旅游风景区磨山樱花园',
                'latitude': 30.5505,
                'longitude': 114.3855,
                'category': '小众景点',
                'description': '世界三大樱花园之一，春季必打卡',
                'rating': 4.8,
                'checkin_count': 26780,
                'status': 1
            }
        ]
        
        added_count = 0
        for spot_data in more_spots:
            existing = CheckinSpot.query.filter_by(name=spot_data['name']).first()
            if not existing:
                spot = CheckinSpot(**spot_data)
                db.session.add(spot)
                added_count += 1
        
        db.session.commit()
        print(f"成功添加 {added_count} 个打卡点！")

if __name__ == '__main__':
    add_more_spots()
