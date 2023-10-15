import wtforms

from wtforms.validators import Email, length, EqualTo,input_required

#  导入数据库user模型
from models import UserModel, EmailCaptchaModel


#  EqualTo : 和那个字段相等


# 注册校验
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    captcha = wtforms.StringField(validators=[length(min=4, max=4, message="验证码有误!")])
    username = wtforms.StringField(validators=[length(min=3, max=18, message="用户名长度有误!")])
    password = wtforms.StringField(validators=[length(min=6, max=18, message="密码长度有误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致!")])

    # 自定义验证
    #  1. 用户输入的邮箱账号是否已经存在
    #  2. 邮箱验证码和邮箱账号是否一致

    def validate_email(self, field):
        #  获取用户输入的邮箱账号
        email = field.data
        #  判断邮箱账号是否已经存在
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("邮箱账号已经存在")

    def validate_captcha(self, field):
        #  获取用户输入的验证码
        captcha = field.data
        email = self.email.data
        result = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not result:
            raise wtforms.ValidationError("验证码错误")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    password = wtforms.StringField(validators=[length(min=6, max=18, message="密码长度有误!")])


class Questions(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=100, message="标题长度有误!")])
    content = wtforms.StringField(validators=[length(min=3, max=10000, message="内容长度有误!")])


class Answers(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=3, max=10000, message="内容长度有误!")])
    question_id = wtforms.IntegerField(validators=[input_required(message="必须传入问题ID:")])