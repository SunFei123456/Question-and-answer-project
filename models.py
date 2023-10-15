from exts import db

from datetime import datetime


# 用户数据模型
class UserModel(db.Model):
    __tablename__ = "user"
    # 添加字段 id字段 primary_key=True 表示主键 autoincrement=True 表示自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # nullable=False 表示非空 unique=True 表示唯一
    email = db.Column(db.String(20), nullable=False, )
    avatar = db.Column(db.String(200))
    join_time = db.Column(db.DateTime, default=datetime.now())


# 邮箱校验模型
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_Captcha"
    # 添加字段 id字段 primary_key=True 表示主键 autoincrement=True 表示自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # nullable=False 表示非空 unique=True 表示唯一
    email = db.Column(db.String(20), nullable=False, unique=True)
    captcha = db.Column(db.String(100), nullable=False)


# 问题模型

class QuestionsModel(db.Model):
    __tablename__ = "question"
    #  id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标题
    title = db.Column(db.String(100), nullable=False)
    # 内容
    content = db.Column(db.Text, nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键连接
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    author = db.relationship(UserModel, backref="questions")


# 答案模型
class AnswerModel(db.Model):
    __tableName__ = "answer"
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 内容
    content = db.Column(db.Text, nullable=False)
    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键连接
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系
    question = db.relationship(QuestionsModel, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")
