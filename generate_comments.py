import sys
import os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.CheckinSpot import CheckinSpot
from models.VisitReport import VisitReport
from models.User import User

def generate_comments_for_new_spots():
    with app.app_context():
        print("为新添加的打卡点生成评论...")

        new_spot_names = [
            '武汉长江大桥', '户部巷', '汉口江滩', '武汉大学', '湖北省美术馆',
            '武汉植物园', '光谷广场', '知音号', '武汉科技馆', '汉正街',
            '湖北美术馆', 'Manner Coffee(武汉恒隆店)', '武汉东湖磨山景区',
            '新华书店(江汉路店)', '武汉欢乐谷', '江汉关博物馆',
            'Today便利店(花园道店)', '武汉长江二桥', '万林艺术博物馆', '东湖樱花园'
        ]

        users = User.query.all()
        if not users:
            print("没有找到用户，请先创建用户")
            return

        user_ids = [u.user_id for u in users]

        comments_templates = [
            {"title": "非常棒的体验！", "content": "这个地方真的很不错！风景优美，设施完善，非常适合拍照打卡。强烈推荐大家来看看！", "rating": 5.0},
            {"title": "值得一去", "content": "总体感觉还可以，景色很美，就是人有点多。建议大家工作日来人会少一些。", "rating": 4.5},
            {"title": "不错的探店之旅", "content": "和朋友一起来玩的，整体体验很好。周边设施齐全，停车也方便。下次还会再来！", "rating": 4.8},
            {"title": "一般般吧", "content": "可能期望太高了，实际感觉一般。不过拍照还是挺好看的。", "rating": 3.5},
            {"title": "超级推荐！", "content": "太喜欢这个地方了！氛围很好，超级出片！一定要来打卡！", "rating": 5.0},
            {"title": "休闲好去处", "content": "周末过来放松一下真的很不错。环境优美，空气清新。", "rating": 4.6},
            {"title": "有点失望", "content": "感觉没有想象中那么好，可能需要改进一下。不过拍照还是可以的。", "rating": 3.8},
            {"title": "绝绝子！", "content": "太棒了！必须给满分！每个角落都很精致，强烈推荐给各位！", "rating": 5.0},
            {"title": "还不错的体验", "content": "整体还行，风景不错，设施也可以。适合拍照和休闲。", "rating": 4.2},
            {"title": "强烈推荐！", "content": "必须给这家店点赞！服务好，环境佳，超级满意！", "rating": 4.9},
            {"title": "一般", "content": "体验一般，没有什么特别的。可能不太适合我。", "rating": 3.0},
            {"title": "超出预期！", "content": "真的超出我的预期！太惊喜了，下次一定会再来！", "rating": 4.7},
            {"title": "拍照圣地", "content": "这个地方太适合拍照了！随便一拍都是大片的感觉！", "rating": 4.8},
            {"title": "环境优美", "content": "环境真的很棒，空气清新，很适合散步放松。", "rating": 4.5},
            {"title": "值得推荐", "content": "整体体验不错，性价比很高。推荐大家来试试！", "rating": 4.4},
            {"title": "不太推荐", "content": "可能是我个人喜好问题，感觉一般。不是特别推荐。", "rating": 2.5},
            {"title": "完美！", "content": "完美的一次体验！每个细节都很棒！必须给五星好评！", "rating": 5.0},
            {"title": "休闲舒适", "content": "很舒适的一个地方，适合和朋友一起来聊天放松。", "rating": 4.3},
            {"title": "打卡成功", "content": "终于来这里打卡了！真的很不错，没有让我失望！", "rating": 4.6},
            {"title": "下次还来", "content": "不错的体验，下次还会再来。支持一下！", "rating": 4.5}
        ]

        added_count = 0
        for spot_name in new_spot_names:
            spot = CheckinSpot.query.filter_by(name=spot_name).first()
            if spot:
                num_comments = random.randint(2, 5)
                for i in range(num_comments):
                    template = random.choice(comments_templates)
                    user_id = random.choice(user_ids)

                    days_ago = random.randint(1, 30)
                    hours_ago = random.randint(0, 23)
                    create_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

                    comment = VisitReport(
                        user_id=user_id,
                        spot_id=spot.spot_id,
                        title=template["title"],
                        content=template["content"],
                        rating=template["rating"],
                        status=1,
                        create_time=create_time
                    )
                    db.session.add(comment)
                    added_count += 1

                spot_rating = sum([t["rating"] for t in random.sample(comments_templates, min(num_comments, len(comments_templates)))]) / num_comments
                spot.rating = round(spot_rating, 1)
                print(f"已为 {spot_name} 添加 {num_comments} 条评论")
            else:
                print(f"未找到打卡点: {spot_name}")

        db.session.commit()
        print(f"\n成功添加 {added_count} 条评论！")

if __name__ == '__main__':
    generate_comments_for_new_spots()
