from flask import Flask, redirect, request
import requests
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access them using os.environ
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)

# Cấu hình app_id và app_secret của anh
 # Đã cấu hình trong Lark Developer Console

@app.route('/')
def home():
    return '<a href="/login">Đăng nhập với Lark</a>'

@app.route('/login')
def login():
    state = 'abc123'  # Có thể thay bằng uuid cho an toàn hơn
    # Tạo URL redirect người dùng đến trang đăng nhập của Lark
    url = f"https://open.larksuite.com/open-apis/authen/v1/index?app_id={APP_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code"
    return redirect(url)

@app.route('/oauth/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if not code:
        return f'❌ Không nhận được mã code! Query String: {request.query_string}'

    # Gửi POST request để đổi code lấy access_token
    token_url = "https://open.larksuite.com/open-apis/authen/v1/access_token"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    response = requests.post(token_url, headers=headers, json=data)
    res_json = response.json()

    if response.status_code == 200 and 'data' in res_json:
        access_token = res_json['data']['access_token']
        open_id = res_json['data'].get('open_id', '')
        return f'''
            ✅ Đăng nhập thành công!<br>
            <strong>Access Token:</strong> {access_token}<br>
            <strong>Open ID:</strong> {open_id}
        '''
    else:
        return f'❌ Lỗi khi lấy access token: {res_json}'

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

