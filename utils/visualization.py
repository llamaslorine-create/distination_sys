import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from models.Novel import Novel
from models.Category import Category
from models.Comment import Comment
from db import db


def generate_novel_category_pie():
    """生成小说分类分布饼图
    
    Returns:
        str: 饼图的base64编码字符串
    """
    # 获取分类数据
    categories = Category.query.filter_by(status=1).all()
    category_data = {}
    
    # 统计每个分类的小说数量
    for category in categories:
        count = Novel.query.filter_by(category_id=category.category_id, status=1).count()
        if count > 0:
            category_data[category.category_name] = count
    
    # 创建饼图
    plt.figure(figsize=(8, 6))
    if category_data:
        plt.pie(category_data.values(), labels=category_data.keys(), autopct='%1.1f%%')
        plt.title('小说分类分布')
    else:
        plt.text(0.5, 0.5, '暂无数据', ha='center', va='center')
    
    # 转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return f'data:image/png;base64,{image_base64}'


def generate_score_trend_line():
    """生成评分趋势折线图
    
    Returns:
        str: 折线图的base64编码字符串，无数据时返回None
    """
    # 获取已审核的评论数据
    comments = Comment.query.filter_by(audit_status=1).all()
    if not comments:
        return None
    
    # 按月份分组统计平均评分
    data = []
    for comment in comments:
        month = comment.create_time.strftime('%Y-%m')
        data.append({'month': month, 'score': comment.score})
    
    # 使用pandas进行数据处理
    df = pd.DataFrame(data)
    monthly_avg = df.groupby('month')['score'].mean().reset_index()
    
    # 创建折线图
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='month', y='score', data=monthly_avg, marker='o')
    plt.title('小说评分趋势')
    plt.xlabel('月份')
    plt.ylabel('平均评分')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return f'data:image/png;base64,{image_base64}'


def generate_novel_word_count_bar():
    """生成小说字数分布柱状图
    
    Returns:
        str: 柱状图的base64编码字符串，无数据时返回None
    """
    # 获取激活的小说数据
    novels = Novel.query.filter_by(status=1).all()
    if not novels:
        return None
    
    # 按字数范围分组
    word_ranges = {'0-10万': 0, '10-50万': 0, '50-100万': 0, '100万以上': 0}
    
    # 统计各字数范围的小说数量
    for novel in novels:
        words = novel.total_words
        if words < 100000:
            word_ranges['0-10万'] += 1
        elif words < 500000:
            word_ranges['10-50万'] += 1
        elif words < 1000000:
            word_ranges['50-100万'] += 1
        else:
            word_ranges['100万以上'] += 1
    
    # 创建柱状图
    plt.figure(figsize=(8, 6))
    plt.bar(word_ranges.keys(), word_ranges.values())
    plt.title('小说字数分布')
    plt.xlabel('字数范围')
    plt.ylabel('小说数量')
    
    # 转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return f'data:image/png;base64,{image_base64}'