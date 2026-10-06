from flask import Flask, request, render_template
import requests
from datetime import datetime
import os

app = Flask(__name__)


# =========================
# 中韓翻譯題庫
# =========================

zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}


# =========================
# 首頁
# =========================

@app.route('/')
def index():
    return render_template('index.html')


# =========================
# 競賽
# =========================

@app.route('/competition')
def competition():
    return render_template('competition.html')


# =========================
# 中韓翻譯
# =========================

@app.route('/ask', methods=['GET', 'POST'])
def ask():

    if request.method == 'POST':

        # 取得使用者輸入
        question1 = request.form.get('question', '').strip()

        # 查詢題庫
        answer1 = zh_ko_dict.get(
            question1,
            "抱歉，我目前沒有這個詞的韓文對應。"
        )

        # 回傳結果
        return render_template(
            'ask.html',
            question=question1,
            answer=answer1
        )

    # GET
    return render_template(
        'ask.html',
        question="",
        answer=""
    )


# =========================
# 課外活動
# =========================

@app.route('/activities', methods=['GET', 'POST'])
def activities():

    if request.method == 'POST':

        question = request.form.get(
            'question',
            ''
        ).strip()

        answer1 = "抱歉，我目前沒有這個詞的韓文對應。"

        return render_template(
            'activities.html',
            question=question,
            answer=answer1
        )

    return render_template(
        'activities.html',
        question="",
        answer=""
    )


# =========================
# 股票查詢
# =========================

@app.route('/stock', methods=['GET', 'POST'])
def stock():

    # GET
    if request.method == 'GET':
        return render_template(
            'stock.html',
            question="",
            answer=""
        )

    # POST
    stock_no = request.form.get(
        'question',
        ''
    ).strip()

    # 沒有輸入股票代號
    if not stock_no:
        return render_template(
            'stock.html',
            question="",
            answer="請輸入股票代號，例如：2330"
        )

    try:

        # 取得目前月份
        today = datetime.now()

        date_str = today.strftime("%Y%m01")

        # TWSE API
        url = (
            "https://www.twse.com.tw/"
            "exchangeReport/STOCK_DAY"
        )

        params = {
            "response": "json",
            "stockNo": stock_no,
            "date": date_str
        }

        # 發送請求
        res = requests.get(
            url,
            params=params,
            timeout=10
        )

        # 轉成 JSON
        data = res.json()

        # 判斷 API 是否成功
        if data.get("stat") == "OK":

            stock_data = data.get("data", [])

            if stock_data:

                # 最後一筆資料
                latest_data = stock_data[-1]

                # 收盤價通常在第 7 欄
                answer = latest_data[6]

                answer = (
                    f"股票代號：{stock_no}<br>"
                    f"最新交易日：{latest_data[0]}<br>"
                    f"收盤價：{answer}"
                )

            else:

                answer = (
                    "查無股票資料，"
                    "請確認股票代號是否正確。"
                )

        else:

            answer = (
                "查無資料，請確認股票代號。"
            )

    except requests.exceptions.RequestException:

        answer = (
            "目前無法連線到股票資料網站，"
            "請稍後再試。"
        )

    except Exception as e:

        print("股票 API 錯誤：", e)

        answer = (
            "取得股票資料時發生錯誤，"
            "請稍後再試。"
        )

    # 回傳結果
    return render_template(
        'stock.html',
        question=stock_no,
        answer=answer
    )


# =========================
# 學習歷程
# =========================

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


# =========================
# 社團
# =========================

@app.route('/club')
def club():
    return render_template('club.html')


# =========================
# 選修課程
# =========================

@app.route('/electives')
def electives():
    return render_template('electives.html')


# =========================
# AI
# =========================

@app.route('/ai')
def ai():
    return render_template('ai.html')


# =========================
# 電子書
# =========================

@app.route('/ebooks')
def ebooks():
    return render_template('ebooks.html')


# =========================
# 電子書舊網址
# /html 也可以進入電子書
# =========================

@app.route('/html')
def html():
    return render_template('ebooks.html')


# =========================
# 啟動 Flask
# =========================

if __name__ == '__main__':

    port = int(
        os.environ.get(
            'PORT',
            5000
        )
    )

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
