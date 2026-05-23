import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.VisitReport import VisitReport
from models.CheckinSpot import CheckinSpot
from models.User import User
from datetime import datetime, timedelta

def add_sample_comments():
    with app.app_context():
        print("添加示例评论数据...")
        
        # 获取现有的用户和打卡点
        user = User.query.filter_by(username='testuser').first()
        if not user:
            print("请先添加测试用户")
            return
        
        spots = CheckinSpot.query.all()
        if not spots:
            print("请先添加打卡点数据")
            return
        
        # 示例评论数据
        comments = {
            1: [
                {"content": "黄鹤楼真的太美了！登楼远眺，长江两岸的景色尽收眼底，尤其是傍晚时分，夕阳洒在江面上，美如画。强烈推荐来武汉一定要来这里看看！", "rating": 5},
                {"content": "门票价格适中，园区很大，可以慢慢逛。建议早点来，避开旅游团高峰。", "rating": 4},
                {"content": "千古名楼，文化底蕴深厚，值得一游。", "rating": 5},
            ],
            2: [
                {"content": "楚河汉街的夜景特别漂亮，灯光璀璨，很适合拍照打卡。这里的建筑风格很有特色，民国风情浓厚。", "rating": 5},
                {"content": "购物、吃饭、看电影都很方便，是武汉最繁华的商圈之一。", "rating": 4},
            ],
            3: [
                {"content": "东湖绿道真是跑步和骑行的好地方！风景优美，空气清新，沿着湖边骑行感觉特别舒服。", "rating": 5},
                {"content": "强烈推荐租一辆自行车环湖骑行，大约需要2-3小时，沿途风景美不胜收。", "rating": 5},
                {"content": "武汉人的后花园，周末休闲的好去处。", "rating": 4},
            ],
            4: [
                {"content": "黎黄陂路的老建筑很有历史感，适合喜欢拍照的朋友来打卡。", "rating": 4},
                {"content": "文艺气息浓厚，有很多咖啡馆和小店可以逛。", "rating": 4},
            ],
            5: [
                {"content": "昙华林太适合文艺青年了！各种特色小店、咖啡馆、书店，拍照超出片。", "rating": 5},
                {"content": "周末人有点多，但整体氛围很好，值得一来。", "rating": 4},
            ],
            10: [
                {"content": "湖北省博物馆太棒了！曾侯乙编钟、越王勾践剑、元青花四爱图梅瓶，三大镇馆之宝一定要看！", "rating": 5},
                {"content": "免费参观，但是需要提前预约。建议安排半天时间慢慢看。", "rating": 5},
                {"content": "文物修复展览很有意思，可以看到文物修复的过程。", "rating": 4},
            ],
        }
        
        added_count = 0
        for spot_id, spot_comments in comments.items():
            spot = CheckinSpot.query.get(spot_id)
            if not spot:
                continue
            
            for comment_data in spot_comments:
                # 检查是否已存在相同评论
                existing = VisitReport.query.filter_by(
                    spot_id=spot_id,
                    user_id=user.user_id,
                    content=comment_data['content']
                ).first()
                
                if not existing:
                    report = VisitReport(
                        spot_id=spot_id,
                        user_id=user.user_id,
                        title='',
                        content=comment_data['content'],
                        rating=comment_data['rating'],
                        status=1,
                        create_time=datetime.now() - timedelta(days=added_count % 7)
                    )
                    db.session.add(report)
                    added_count += 1
        
        db.session.commit()
        print(f"成功添加 {added_count} 条示例评论！")

if __name__ == '__main__':
    add_sample_comments()
