import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.User import User
from models.CheckinSpot import CheckinSpot
import bcrypt

def init_data():
    with app.app_context():
        print("初始化数据...")
        
        if not User.query.filter_by(user_id=1).first():
            print("添加测试用户...")
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
            user = User(
                user_id=1,
                username='testuser',
                password=hashed_password.decode('utf-8'),
                nickname='测试用户',
                email='test@example.com',
                status=1
            )
            db.session.add(user)
            db.session.commit()
            print("测试用户添加成功")
        
        CheckinSpot.query.delete()
        db.session.commit()
        
        spots = [
            {
                'spot_id': 1,
                'name': '黄鹤楼',
                'address': '武汉市武昌区蛇山西山坡特1号',
                'latitude': 30.5433,
                'longitude': 114.3053,
                'category': '小众景点',
                'description': '江南三大名楼之一，武汉地标性建筑',
                'rating': 4.5,
                'checkin_count': 23880
            },
            {
                'spot_id': 2,
                'name': '楚河汉街',
                'address': '武汉市武昌区东湖路108号',
                'latitude': 30.5547,
                'longitude': 114.3282,
                'category': '小众景点',
                'description': '民国风格的商业步行街，购物休闲好去处',
                'rating': 4.4,
                'checkin_count': 18760
            },
            {
                'spot_id': 3,
                'name': '东湖绿道',
                'address': '武汉市武昌区东湖生态旅游风景区',
                'latitude': 30.5632,
                'longitude': 114.3647,
                'category': '小众景点',
                'description': '中国最长的5A级城市核心区环湖绿道',
                'rating': 4.7,
                'checkin_count': 15670
            },
            {
                'spot_id': 4,
                'name': '黎黄陂路',
                'address': '武汉市江岸区黎黄陂路',
                'latitude': 30.5878,
                'longitude': 114.2168,
                'category': '小众景点',
                'description': '历史风貌街区，充满老武汉风情',
                'rating': 4.6,
                'checkin_count': 8920
            },
            {
                'spot_id': 5,
                'name': '昙华林',
                'address': '武汉市武昌区昙华林',
                'latitude': 30.5521,
                'longitude': 114.3156,
                'category': '小众景点',
                'description': '文艺青年聚集地，充满艺术气息',
                'rating': 4.5,
                'checkin_count': 12340
            },
            {
                'spot_id': 6,
                'name': '星巴克臻选(武汉天地店)',
                'address': '武汉市江岸区武汉天地',
                'latitude': 30.5832,
                'longitude': 114.2235,
                'category': '咖啡馆',
                'description': '环境优雅的星巴克臻选店',
                'rating': 4.8,
                'checkin_count': 3456
            },
            {
                'spot_id': 7,
                'name': '西西弗书店(凯德广场店)',
                'address': '武汉市硚口区解放大道凯德广场',
                'latitude': 30.5658,
                'longitude': 114.2523,
                'category': '书店',
                'description': '集阅读与咖啡于一体的连锁书店',
                'rating': 4.7,
                'checkin_count': 2890
            },
            {
                'spot_id': 8,
                'name': '猫的天空之城概念书店',
                'address': '武汉市武昌区楚河汉街',
                'latitude': 30.5528,
                'longitude': 114.3265,
                'category': '书店',
                'description': '文艺书店，提供明信片邮寄服务',
                'rating': 4.6,
                'checkin_count': 4567
            },
            {
                'spot_id': 9,
                'name': '武汉美术馆',
                'address': '武汉市江岸区中山大道保华街2号',
                'latitude': 30.5821,
                'longitude': 114.2075,
                'category': '美术馆',
                'description': '国家级美术馆，定期举办艺术展览',
                'rating': 4.5,
                'checkin_count': 6780
            },
            {
                'spot_id': 10,
                'name': '湖北省博物馆',
                'address': '武汉市武昌区东湖路156号',
                'latitude': 30.5685,
                'longitude': 114.3562,
                'category': '小众景点',
                'description': '国家一级博物馆，曾侯乙编钟故乡',
                'rating': 4.8,
                'checkin_count': 28900
            },
            {
                'spot_id': 11,
                'name': '古德寺',
                'address': '武汉市江岸区黄浦大街上滑坡路74号',
                'latitude': 30.6072,
                'longitude': 114.2435,
                'category': '小众景点',
                'description': '融欧亚宗教建筑风格于一体的寺庙',
                'rating': 4.6,
                'checkin_count': 9870
            },
            {
                'spot_id': 12,
                'name': 'K11购物艺术中心',
                'address': '武汉市硚口区解放大道628号',
                'latitude': 30.5678,
                'longitude': 114.2535,
                'category': '文创店',
                'description': '艺术与商业融合的购物中心',
                'rating': 4.5,
                'checkin_count': 15430
            },
            {
                'spot_id': 13,
                'name': '武汉万达电影乐园',
                'address': '武汉市武昌区水果湖街东湖路138号',
                'latitude': 30.5587,
                'longitude': 114.3312,
                'category': '小众景点',
                'description': '高科技主题乐园',
                'rating': 4.3,
                'checkin_count': 7650
            },
            {
                'spot_id': 14,
                'name': '壹方购物中心',
                'address': '武汉市江岸区中山大道1515号',
                'latitude': 30.5845,
                'longitude': 114.2185,
                'category': '文创店',
                'description': '高端购物中心，众多国际品牌',
                'rating': 4.6,
                'checkin_count': 12340
            },
            {
                'spot_id': 15,
                'name': '桃园眷村',
                'address': '武汉市江汉区解放大道688号',
                'latitude': 30.5728,
                'longitude': 114.2285,
                'category': '餐厅',
                'description': '台湾风味早餐店，文艺装修风格',
                'rating': 4.4,
                'checkin_count': 5670
            }
        ]
        
        print("添加武汉市打卡点数据...")
        for spot_data in spots:
            spot = CheckinSpot(**spot_data)
            db.session.add(spot)
        
        db.session.commit()
        print("武汉市打卡点数据添加成功！")

if __name__ == '__main__':
    init_data()