"""一次性脚本：
1. 批量导入 28 个武汉打卡点（按 name 去重）
2. 给每个打卡点造 2-5 条 VisitReport（评论），作者从现有用户里随机选
"""
import sys, os, random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app
from db import db
from models.CheckinSpot import CheckinSpot
from models.VisitReport import VisitReport
from models.User import User


SPOTS = [
    (1,  '黄鹤楼',                       '小众景点', '湖北省武汉市武昌区蛇山西坡特1号',                    30.5444, 114.2980),
    (2,  '东湖绿道',                     '小众景点', '湖北省武汉市武昌区东湖生态旅游风景区',               30.5588, 114.3684),
    (3,  '湖北省博物馆',                 '小众景点', '湖北省武汉市武昌区东湖路160号',                       30.5635, 114.3621),
    (4,  '楚河汉街',                     '文创店',   '湖北省武汉市武昌区中北路171号',                       30.5562, 114.3328),
    (5,  '昙华林',                       '小众景点', '湖北省武汉市武昌区昙华林路',                          30.5455, 114.3063),
    (6,  '武汉工程大学',                 '小众景点', '湖北省武汉市东湖新技术开发区光谷一路206号',           30.4820, 114.4221),
    (7,  '星巴克臻选(武汉天地店)',       '咖啡馆',   '湖北省武汉市江岸区中山大道1622号武汉天地',            30.6103, 114.3089),
    (8,  '西西弗书店(凯德广场店)',       '书店',     '湖北省武汉市硚口区中山大道238号凯德广场',             30.5741, 114.2645),
    (9,  '武汉长江大桥',                 '小众景点', '武汉市武昌区临江大道与龟山南路交汇处',                30.5496, 114.2886),
    (10, '户部巷',                       '餐厅',     '武汉市武昌区自由路',                                  30.5437, 114.2968),
    (11, '汉口江滩',                     '小众景点', '武汉市江岸区沿江大道',                                30.5945, 114.3025),
    (12, '武汉大学',                     '小众景点', '武汉市武昌区珞喻路129号',                             30.5416, 114.3663),
    (13, '湖北省美术馆',                 '美术馆',   '武汉市武昌区东湖路三官殿1号',                         30.5619, 114.3598),
    (14, '武汉植物园',                   '小众景点', '武汉市洪山区鲁磨路特1号',                             30.5429, 114.4121),
    (15, '光谷广场',                     '文创店',   '武汉市洪山区珞喻路光谷广场',                          30.5060, 114.4104),
    (16, '知音号',                       '小众景点', '武汉市江岸区沿江大道江滩公园知音号码头',              30.5992, 114.3067),
    (17, '武汉科技馆',                   '小众景点', '武汉市江岸区沿江大道91号',                            30.5819, 114.2986),
    (18, '汉正街',                       '文创店',   '武汉市硚口区汉正街',                                  30.5710, 114.2796),
    (19, '湖北美术馆',                   '美术馆',   '武汉市武昌区中山路368号',                             30.5436, 114.2962),
    (20, 'Manner Coffee(武汉恒隆店)',    '咖啡馆',   '武汉市硚口区京汉大道668号武汉恒隆广场',               30.5794, 114.2731),
    (21, '武汉东湖磨山景区',             '小众景点', '武汉市武昌区东湖生态旅游风景区磨山',                  30.5519, 114.4063),
    (22, '新华书店(江汉路店)',           '书店',     '武汉市江汉区江汉路257号',                             30.5797, 114.2860),
    (23, '武汉欢乐谷',                   '小众景点', '武汉市洪山区东湖生态旅游风景区欢乐大道196号',         30.5876, 114.3978),
    (24, '江汉关博物馆',                 '小众景点', '武汉市江岸区沿江大道129号',                           30.5778, 114.2962),
    (25, 'Today便利店(花园道店)',        '餐厅',     '武汉市江汉区青年路308号花园道',                       30.5914, 114.2647),
    (26, '武汉长江二桥',                 '小众景点', '武汉市江岸区沿江大道',                                30.6144, 114.3242),
    (27, '万林艺术博物馆',               '美术馆',   '武汉市武昌区珞喻路129号武汉大学内',                   30.5419, 114.3658),
    (28, '东湖樱花园',                   '小众景点', '武汉市武昌区东湖生态旅游风景区磨山樱花园',            30.5512, 114.4086),
]


COMMENT_TEMPLATES = [
    {'title': '非常棒的体验！',  'content': '这个地方真的很不错！风景优美，设施完善，非常适合拍照打卡。强烈推荐大家来看看！', 'rating': 5.0},
    {'title': '值得一去',        'content': '总体感觉还可以，景色很美，就是人有点多。建议大家工作日来人会少一些。',                'rating': 4.5},
    {'title': '不错的探店之旅',  'content': '和朋友一起来玩的，整体体验很好。周边设施齐全，停车也方便。下次还会再来！',          'rating': 4.8},
    {'title': '一般般吧',        'content': '可能期望太高了，实际感觉一般。不过拍照还是挺好看的。',                              'rating': 3.5},
    {'title': '超级推荐！',      'content': '太喜欢这个地方了！氛围很好，超级出片！一定要来打卡！',                              'rating': 5.0},
    {'title': '休闲好去处',      'content': '周末过来放松一下真的很不错。环境优美，空气清新。',                                  'rating': 4.6},
    {'title': '有点失望',        'content': '感觉没有想象中那么好，可能需要改进一下。不过拍照还是可以的。',                      'rating': 3.8},
    {'title': '绝绝子！',        'content': '太棒了！必须给满分！每个角落都很精致，强烈推荐给各位！',                            'rating': 5.0},
    {'title': '还不错的体验',    'content': '整体还行，风景不错，设施也可以。适合拍照和休闲。',                                  'rating': 4.2},
    {'title': '强烈推荐！',      'content': '必须给这家店点赞！服务好，环境佳，超级满意！',                                      'rating': 4.9},
    {'title': '一般',            'content': '体验一般，没有什么特别的。可能不太适合我。',                                        'rating': 3.0},
    {'title': '超出预期！',      'content': '真的超出我的预期！太惊喜了，下次一定会再来！',                                      'rating': 4.7},
    {'title': '拍照圣地',        'content': '这个地方太适合拍照了！随便一拍都是大片的感觉！',                                    'rating': 4.8},
    {'title': '环境优美',        'content': '环境真的很棒，空气清新，很适合散步放松。',                                          'rating': 4.5},
    {'title': '值得推荐',        'content': '整体体验不错，性价比很高。推荐大家来试试！',                                        'rating': 4.4},
    {'title': '完美！',          'content': '完美的一次体验！每个细节都很棒！必须给五星好评！',                                  'rating': 5.0},
    {'title': '休闲舒适',        'content': '很舒适的一个地方，适合和朋友一起来聊天放松。',                                      'rating': 4.3},
    {'title': '打卡成功',        'content': '终于来这里打卡了！真的很不错，没有让我失望！',                                      'rating': 4.6},
    {'title': '下次还来',        'content': '不错的体验，下次还会再来。支持一下！',                                              'rating': 4.5},
]


def import_spots():
    inserted, skipped = [], []
    for _, name, category, address, lat, lng in SPOTS:
        if CheckinSpot.query.filter_by(name=name).first():
            skipped.append(name)
            continue
        spot = CheckinSpot(
            name=name, category=category, address=address,
            latitude=lat, longitude=lng,
            description=f'位于{address}的{category}',
            rating=0.0, checkin_count=0, status=1,
        )
        db.session.add(spot)
        inserted.append(name)
    db.session.commit()
    return inserted, skipped


def seed_comments():
    users = User.query.all()
    if not users:
        print('[WARN] 数据库里没有任何用户，无法造评论')
        return 0
    user_ids = [u.user_id for u in users]
    spot_names = [name for _, name, *_ in SPOTS]
    added = 0
    for name in spot_names:
        spot = CheckinSpot.query.filter_by(name=name).first()
        if not spot:
            continue
        n = random.randint(2, 5)
        picked = random.sample(COMMENT_TEMPLATES, n)
        for t in picked:
            days_ago = random.randint(1, 30)
            hours_ago = random.randint(0, 23)
            create_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
            db.session.add(VisitReport(
                user_id=random.choice(user_ids),
                spot_id=spot.spot_id,
                title=t['title'], content=t['content'], rating=t['rating'],
                status=1, create_time=create_time,
            ))
            added += 1
        spot.rating = round(sum(t['rating'] for t in picked) / n, 1)
    db.session.commit()
    return added


if __name__ == '__main__':
    with app.app_context():
        inserted, skipped = import_spots()
        print(f'[导入] 新增 {len(inserted)} 个：{inserted}')
        print(f'[导入] 跳过 {len(skipped)} 个（重名）：{skipped}')
        added = seed_comments()
        print(f'[评论] 共新增 {added} 条 VisitReport')
        print('[OK] 完成')
