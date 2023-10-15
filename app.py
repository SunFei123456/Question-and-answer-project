# g 为全局对象 可以存储值
from flask import Flask, session, g

# 导入数据库迁移管理包
from flask_migrate import Migrate

# 导入config.py文件
import config

# 导入扩展文件
from exts import db
from exts import mail

# 导入蓝图文件(视窗函数)
from blueprints.Qq import bp as qa_bp
from blueprints.auth import bp as auth_bp

# app里面需要User模型
from models import UserModel

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 先创建db空参实例对象,后传入app 与app进行绑定
db.init_app(app)

mail.init_app(app)

migrate = Migrate(app, db)
# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


@app.before_request
def my_before_request():
    userID = session.get("user_id")
    if userID:
        user = UserModel.query.get(userID)
        setattr(g, "user", user)
    else:
        setattr(g, 'user', None)


@app.context_processor
def my_context_processor():
    # 这样的话就可以在任意模块使用 user这个变量 对应的值是全局对象存储的user值
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
