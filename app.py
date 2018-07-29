from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from models import User,Question,Answer
from exts import db
from sqlalchemy import or_
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username==username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            #如果想在31天内都不需要登录
            bool = request.form.get('bool')
            print(bool)
            if bool == 'on':
                session.permanent = True
            else:
                session.permanent = False
            return redirect(url_for('index'))
        else:
            return u'用户名或者密码错误，请确认后重新登录！'

# @app.before_request


@app.route('/question/',methods=['GET','POST'])
# @app.before_request
def question():
    a = session.get('user_id')
    # print(a)
    if session.get('user_id'):
        if request.method == 'POST':
            title = request.form.get('title')
            context = request.form.get('content')
            authon_id = session.get('user_id')
            # print(authon_id)
            question1 = Question(title=title,content=context, author_id=authon_id)
            db.session.add(question1)
            db.session.commit()
            return redirect(url_for('index'))
            # context
            # return render_template('question.html')
        else:
            return render_template('question.html')
    else:
            return redirect(url_for('login'))


@app.route('/loginout/')
def loginout():
    session.clear()
    # session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 手机号码验证
        if phone == '' or username == '' or password1 == '' or password2 =='':
            return u'以上都必须填写！'
        user = User.query.filter(User.phone == phone).first()

        if user:
            return u'该手机已经被注册，请更换手机号码！'
        else:
            if password2 != password1:
                return u'两次输入的密码不同！'
            else:
                user = User(phone=phone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question_model)

@app.route('/add_answer/',methods=['POST'])
def add_answer():

    if session.get('user_id'):
        content = request.form.get('answer_content')
        question_id = request.form.get('question_id')
        answer = Answer(content=content)
        answer.author = g.user
        question =  Question.query.filter(Question.id == question_id).first()
        answer.question = question
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail', question_id =question_id))
    else:
        return redirect(url_for('login'))

@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html', questions=questions)
# def before_request():
#     print("我勾住了每次请求")
#     user_id = session.get("user_id")
#     if user_id:
#         print('111')
#         pass
#     else:
#         print('222')
#         return redirect(url_for('login'))
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

if __name__  ==  '__main__':
    app.run()

