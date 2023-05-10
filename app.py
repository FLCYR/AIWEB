import datetime
from flask import Flask,render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
from mysql.config import BaseConfig
from sqlalchemy import and_
from flask_mail import Mail,Message
import random
import hashlib
from sqlalchemy import text

app=Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
mail = Mail(app)
REGISTER_CODE = {'email':'code'}
@app.route('/getComment',methods=['GET'])
def get_comments():


    article_id = request.args.get('article_id')
    try:
        article_id = int(article_id)
    except:
        article_id = 0
    print('id',article_id)
    childList = []
    objs = []
    comment_ids = Comment.query.filter(and_(Comment.parent_id==-1,Comment.article_id==article_id)).all()
    print('ids:',comment_ids)
    for item in comment_ids:
        cid = item.comment_id
        comments = Comment.query.filter(Comment.parent_id==cid).all()
        for c in comments:
            child = {'id':c.comment_id,'name':c.user_name,'content':c.content}
            childList.append(child)
            print(child)

        obj = {'id':item.comment_id,'name': item.user_name,'content':item.content,'child':childList}
        objs.append(obj)
        childList = []
    print(objs)
    return jsonify(objs)


@app.route('/saveComment',methods=['POST'])
def save_comment():

    data = request.get_json()
    print('data: ',data)
    parent_id = data['parent_id']
    user_name = data['user_name']
    email = data['email']
    content = data['content']
    article_id = data['article_id']
    created_at = datetime.datetime.now().timestamp()
    comment  = Comment(parent_id=parent_id,user_name=user_name,email=email,content=content,article_id=article_id,created_at=created_at)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'code':200,'msg':'success'})



@app.route('/',methods=['GET','POST'])
def index_page():
    return render_template('index.html')



# /getPicturePageAndLimit?page=1&limit=20
@app.route('/ai-images',methods=['GET'])
def get_picture_page_and_limit():

    path = 'http://39.108.71.11:8001/images'
    page = request.args.get('page')
    limit = request.args.get('limit')
    try:
        page = int(page)
        limit = int(limit)
    except:
        page = 1
        limit = 20

    start = (page-1)*limit
    num= limit

    res_sql= f"select uri from image limit {start},{num}"
    res = db.session.execute(text(res_sql))
    urls = []
    for item in res.scalars():

        abs = '{}/{}'.format(path,item)
        obj = {'name':item,'url':abs}
        urls.append(obj)
    return jsonify(urls)


@app.route('/image',methods=['GET','POST'])
def return_image_urls():
    pass

# /send-code?email=xxx
@app.route('/send-code',methods=['POST'])
def send_email_code():

    email = request.args.get('email')
    print('email:',email)
    res = UserInfo.query.filter(UserInfo.user_name==email).first()
    if res:
        return jsonify({'code':500,'msg':'该邮箱已经注册'})

    code = random.randint(1000, 9999)
    print('code: ',code)
    # send_email(email,code)
    REGISTER_CODE[email] = str(code)
    return jsonify({'code':200,'msg':'send email success'}),200

# 参数 email password(经过md5加密)
# /register?email=xxx&password=xxx&code=xxx
@app.route('/register',methods=['POST'])
def register():

    email = request.args.get('email')
    password = request.args.get('password')
    code = request.args.get('code')

    print('email: ',email)
    print('password: ',password)
    print('code: ',code)
    print('email code:',REGISTER_CODE[email])

    if REGISTER_CODE[email] != code:
        print('验证码错误')
        return jsonify({'code':500,'msg':'验证码错误'}),500

    #使用随机密钥加密password

    # random user_name
    user_name = 'user_{}'.format(random.randint(100000,999999))

    # 保存到数据库
    user = UserInfo(user_name=user_name,sex=3,created_at=datetime.datetime.now().timestamp(),user_desc='')
    auth = EmailAuth(user_id=user.user_id,email=email,password=password)
    db.session.add(user)
    db.session.add(auth)
    db.session.commit()
    # 注册成功
    print('register success')
    return jsonify({'code':200,'msg':'register success'}),200

@app.route('/login',methods=['POST'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    # 使用随机密钥解密password
    res = EmailAuth.query.filter(and_(EmailAuth.email==email,EmailAuth.password==password)).first()
    user_id = res.user_id
    profile = UserInfo.query.filter(UserInfo.user_id==user_id).first()
    if res:
        return jsonify({'code':200,'msg':'login success'}),200
    else:
        return jsonify({'code':500,'msg':'login fail'}),500


# send email
def send_email(email_addr,code):

    msg = Message('AcFunAI Register',sender=app.config["MAIL_USERNAME"],recipients=[email_addr])
    msg.html = render_template('email.html',code=code)
    mail.send(msg)
    # msg = Message(subject, sender='发送文件的QQ邮箱地址', recipients=[to])
    # msg.html = render_template(template + '.txt', user=user, token=token)
    # mail.send(msg)


# create table userInfo(user_id int primary key auto_increment,user_name varchar(255),sex int,created_at float,user_desc text);
class UserInfo(db.Model):
    __tablename__ = 'userInfo'
    user_id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(255))
    sex = db.Column(db.Integer)
    created_at = db.Column(db.Float)
    user_desc = db.Column(db.Text)

# create table emailAuth(id int primary key auto_increment,user_id int,email text,password text);
class EmailAuth(db.Model):
    __tablename__ = 'emailAuth'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    email = db.Column(db.Text)
    password = db.Column(db.Text)


class Image(db.Model):

    __tablename__ = 'image'
    id = db.Column(db.Integer,primary_key=True)
    uri = db.Column(db.String(255))
    name = db.Column(db.String(255))
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)

# create table comments (comment_id int primary key auto_increment, parent_id int, article_id int, user_name varchar(255), email varchar(128),content text, created_at float);
class Comment(db.Model):

        __tablename__ = 'comments'
        comment_id = db.Column(db.Integer,primary_key=True)
        parent_id = db.Column(db.Integer)
        article_id = db.Column(db.Integer)
        user_name = db.Column(db.String(255))
        email = db.Column(db.String(128))
        content = db.Column(db.Text)
        created_at = db.Column(db.Float)


if __name__ == '__main__':

    # TO-DO
    # 修改mysql远程连接

    # app.run(host='0.0.0.0',port=5000,debug=True)  # debug=True
    app.run(host='0.0.0.0',port=3000)  # debug=True
    db.close()


