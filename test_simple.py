from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = 'test-secret-key'

@app.route('/')
def index():
    return render_template_string('<h1>测试成功!</h1>')

@app.route('/login')
def login():
    return render_template_string('''
        <form method="post" action="/do_login">
            <input type="text" name="username" placeholder="用户名">
            <input type="password" name="password" placeholder="密码">
            <button type="submit">登录</button>
        </form>
    ''')

@app.route('/do_login', methods=['POST'])
def do_login():
    return '登录成功'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
