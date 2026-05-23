#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建表并添加示例数据
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from models.CheckinSpot import CheckinSpot
from models.VisitReport import VisitReport
from models.Badge import Badge
from models.User import User
from models.Admin import Admin
from models.BlogPost import BlogPost, BlogComment
from models.Announcement import Announcement
from datetime import datetime

def init_db():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建成功！")
        
        # 添加示例打卡点数据
        spots_data = [
            {
                'name': '黄鹤楼',
                'address': '湖北省武汉市武昌区蛇山西坡特1号',
                'latitude': 30.5433,
                'longitude': 114.3053,
                'category': '小众景点',
                'description': '江南三大名楼之一，武汉地标性建筑',
                'rating': 4.8,
                'checkin_count': 15678
            },
            {
                'name': '东湖绿道',
                'address': '湖北省武汉市武昌区东湖生态旅游风景区',
                'latitude': 30.5500,
                'longitude': 114.3700,
                'category': '小众景点',
                'description': '武汉最美的城市绿道，适合骑行散步',
                'rating': 4.7,
                'checkin_count': 8923
            },
            {
                'name': '湖北省博物馆',
                'address': '湖北省武汉市武昌区东湖路160号',
                'latitude': 30.5523,
                'longitude': 114.3786,
                'category': '小众景点',
                'description': '国家一级博物馆，曾侯乙编钟的故乡',
                'rating': 4.6,
                'checkin_count': 6542
            },
            {
                'name': '楚河汉街',
                'address': '湖北省武汉市武昌区中北路171号',
                'latitude': 30.5427,
                'longitude': 114.3476,
                'category': '文创店',
                'description': '武汉最繁华的商业街之一',
                'rating': 4.5,
                'checkin_count': 12345
            },
            {
                'name': '昙华林',
                'address': '湖北省武汉市武昌区昙华林路',
                'latitude': 30.5400,
                'longitude': 114.3100,
                'category': '小众景点',
                'description': '文艺青年打卡圣地',
                'rating': 4.4,
                'checkin_count': 5678
            },
            {
                'name': '武汉工程大学',
                'address': '湖北省武汉市东湖新技术开发区光谷一路206号',
                'latitude': 30.5236,
                'longitude': 114.4176,
                'category': '小众景点',
                'description': '美丽的大学校园',
                'rating': 4.2,
                'checkin_count': 2345
            },
            {
                'name': '星巴克臻选(武汉天地店)',
                'address': '湖北省武汉市江岸区中山大道1622号武汉天地',
                'latitude': 30.6000,
                'longitude': 114.2900,
                'category': '咖啡馆',
                'description': '武汉顶级星巴克',
                'rating': 4.3,
                'checkin_count': 3456
            },
            {
                'name': '西西弗书店(凯德广场店)',
                'address': '湖北省武汉市硚口区中山大道238号凯德广场',
                'latitude': 30.5800,
                'longitude': 114.2700,
                'category': '书店',
                'description': '温馨的连锁书店',
                'rating': 4.1,
                'checkin_count': 1234
            }
        ]
        
        for spot_data in spots_data:
            if not CheckinSpot.query.filter_by(name=spot_data['name']).first():
                spot = CheckinSpot(**spot_data)
                db.session.add(spot)
        
        db.session.commit()
        print("打卡点数据添加成功！")
        
        # 添加示例博客文章
        blog_posts = [
            {
                'author_name': '旅游达人小王',
                'title': '武汉三日游攻略分享',
                'content': '刚刚从武汉回来，和大家分享一下我的旅游攻略！第一天：黄鹤楼、武汉长江大桥、户部巷；第二天：湖北省博物馆、东湖；第三天：楚河汉街、江汉路步行街。非常充实的一次旅行！',
                'view_count': 1523
            },
            {
                'author_name': '美食探索家',
                'title': '武汉必吃美食推荐',
                'content': '武汉不仅是九省通衢，更是美食之都！热干面、周黑鸭、武昌鱼、糊汤粉...每一样都让人回味无穷！强烈推荐大家去户部巷和万松园品尝美食。',
                'view_count': 892
            }
        ]
        
        for post_data in blog_posts:
            if not BlogPost.query.filter_by(title=post_data['title']).first():
                post = BlogPost(**post_data)
                db.session.add(post)
        
        db.session.commit()
        print("博客文章添加成功！")
        
        # 添加示例公告
        if not Announcement.query.first():
            announcement = Announcement(
                title='欢迎来到武汉城市探店系统',
                content='欢迎大家使用我们的城市探店与打卡地图系统！在这里您可以发现武汉的美丽景点，分享您的旅游经历，和其他游客互动交流。',
                admin_id=1
            )
            db.session.add(announcement)
            db.session.commit()
            print("公告添加成功！")
        
        print("\n数据库初始化完成！")

if __name__ == '__main__':
    init_db()
