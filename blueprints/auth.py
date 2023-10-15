from flask import Blueprint, render_template, jsonify, redirect, url_for, session, g
# 导入flask-mail
from exts import mail, db
from flask_mail import Message

from flask import request
from models import EmailCaptchaModel
import string
import random
from .forms import RegisterForm, LoginForm
from models import UserModel


# 生成加密密码
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/sunfei", template_folder="templates")


# 定义视图函数
# 登录
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            # 数据格式校验成功,然后去数据库进行比较
            email = form.email.data
            password = form.password.data
            #  根据email 进行一个数据库查询
            user = UserModel.query.filter_by(email=email).first()
            # 如果查询的用户不存在数据库里面 说明用户第一次登录,我们可以进行一个提示
            if not user:
                print("用户不存在")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # cookie:
                # cookie 中不适合存储太多的数据,只适合存储少量的数据
                # cookie 一般用来存放登录授权的东西
                # flask 中的session, 是经过加密后存储在cookie中的
                session['user_id'] = user.id
                return redirect('/')
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# 退出登录
@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")


# 注册
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        # 借助一个插件 进行表单的验证 flask-wtf 基于wtforms
        form = RegisterForm(request.form)
        # validate 会自动调用RegisterForm 类面的类型检查器 和定义好的检查方法
        # form.validate() 该方法会返回一个布尔类型
        if form.validate():
            # 上面验证通过,将form表单里面的各项数据进行一个数据库的存储
            email = form.email.data
            username = form.username.data
            password = generate_password_hash(form.password.data)
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            #  注册成功之后,进行页面跳转 ==> 登录页面
            return redirect(url_for("auth.login"))  # 对应上面的login视窗函数
        else:
            print(form.errors)
            # 注册失败,刷新本页面

            return redirect(url_for("auth.register"))


# 没有指定methon请求方式,默认就是GTE请求
@bp.route('/captcha/email')
# /sunfei/captcha/email?email=12345678901@qq.com
# 发送邮箱请求 获取验证码的接口
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits * 4
    captcha = ''.join(random.sample(source, 4))
    message = Message(subject="孙飞课堂验证码", recipients=[email],
                      body=f"[孙飞课堂] 验证码为{captcha}。此验证码只用于进行短信登陆.15分钟内有效")
    mail.send(message)
    # memcached / redis
    #  数据库存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    # result API 风格
    # {code:200/304/404/500, msg:"", data:""}
    return jsonify({"code": 200,
                    "msg": "成功",
                    "data": None})
