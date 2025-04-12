from flask import Flask
from flask import render_template ,request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
#pythonのタイムゾーンライブラリ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

#データベース(個人用)に追加したい要素
#カレンダー
# →実際に保存する要素
#1つ1つのイベントスケジュール（このカラムの１つにどこのカレンダーに属しているかを登録する。）
#ID,イベントの時間,イベント名,ユーザー名,カレンダー名,保存した時間,カレンダーの日付

class Event(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    #event_dateは本当は日付データにしたい
    event_date = db.Column(db.String(50),nullable=False)
    event_name = db.Column(db.String(50),nullable=False)
    event_time = db.Column(db.String(30),nullable=False)
    user_name = db.Column(db.String(30),nullable=False)
    calender_name = db.Column(db.String(30),nullable=False)
    save_date = db.Column(db.DateTime,nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile", methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        my_data = Event.query.all()
        # data = zip(users,days)
        return render_template("profile.html",my_data = my_data)

@app.route("/edit/event_add", methods=['GET','POST'])
def event_add():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        event_time = request.form.get('event_time')
        #仮で名づけておく
        user_name = "supa"
        calender_name = "my_new_calender"
        event_date = "4/20"

        event_object = Event(event_name=event_name,event_time=event_time,user_name=user_name,calender_name=calender_name,event_date=event_date)
        db.session.add(event_object)
        db.session.commit()
        #本当はredirect("/edit")
        return redirect("/")
    else:
        return render_template("event_add.html")

@app.route("/<int:id>/event_edit",methods=['GET','POST'])
def event_edit(id):
    #IDを基にイベントオブジェクトを特定、イベント単位で読み込む
    event = Event.query.get_or_404(id)
    if request.method == 'GET':
        return render_template("event_edit.html", event=event)
    else:
        event.event_name = request.form.get('event_name')
        event.event_time = request.form.get('event_time')
    #上書きするときはcommitだけでよい
        db.session.commit()
        #本当はredirect("/edit")
        return redirect("/")
    
@app.route("/<int:id>/event_delete",methods=['GET'])
def event_delete(id):
    #IDを基にイベントオブジェクトを特定、イベント単位で読み込む
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    #上書きするときはcommitだけでよい
    db.session.commit()
    return redirect("/")
    

#sqlアルケミーでsql文を使わなくてよくなる。
# →ORマッパー,DBの違いを意識しなくてよくなる。

#GET→webページをゲット
#POST→フォームから送信

#requestはwebページに送られるメソッドがどっちであるかを判定