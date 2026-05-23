import sys
import traceback

sys.path.insert(0, 'd:\\novel-1\\novel_sys')

try:
    print("正在导入应用...")
    from app import app
    print("应用导入成功")
    
    print("\n尝试启动应用...")
    app.run(debug=True, port=5000)
    
except Exception as e:
    print(f"启动失败: {e}")
    traceback.print_exc()
