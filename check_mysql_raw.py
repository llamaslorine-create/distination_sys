import pymysql
import sys

# 数据库配置信息
db_config = {
    'host': '127.0.0.1', # 将 localhost 改为 127.0.0.1
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'novel_sys',
    'charset': 'utf8mb4'
}

print(f"尝试通过 pymysql 直接连接数据库: {db_config['db']}@{db_config['host']}")

try:
    # 建立连接
    connection = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        charset=db_config['charset']
    )
    
    try:
        with connection.cursor() as cursor:
            # 1. 测试连接
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("SUCCESS: 基础数据库连接正常！")
            
            # 2. 检查 admin 表是否存在并统计
            try:
                cursor.execute("SELECT COUNT(*) FROM admin")
                count = cursor.fetchone()[0]
                print(f"SUCCESS: admin 表访问正常，共有 {count} 条记录。")
            except Exception as e:
                print(f"WARNING: 访问 admin 表时出错 (可能表不存在): {e}")
                
    finally:
        connection.close()
        print("连接已关闭。")

except Exception as e:
    print("ERROR: 数据库连接失败！")
    print(f"错误详情: {e}")
    sys.exit(1)
