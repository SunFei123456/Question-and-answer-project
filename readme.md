# 知识论坛项目

## 1. 项目背景和目标

开发这个项目,想到了平时经常询问ChatGPT 学习或者生活上的问题, 但是大部分GPT网站保存会话都是一整个上下文会话, 无法单独抽出保存一个问题. 日后只能去翻找,很麻烦.

通过这个知识论坛,不仅可以将平时询问GPT 有意义有价值的问题给记录下来,同时也很方便日后翻看查找学习.

## 2. 技术架构

前端: html css js 三件套 以及 Ajax的使用

后端: python,

第三方库: flask, flask_sqlalchemy,flask_mail,flask_migrate,werkzeug.security....

数据库: mysql

## 3. 功能模块

1. 注册登录
2. 首页(问题展示)
3. 发布问题
4. 评论
5. 关键字搜索

## 4. 开发过程

### 4.1 注册模块(前端方面)

**视图 接口**

```python
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
```

**数据库模型(注册数据存储)**

id -- 用户名 -- 密码 --  邮箱 --  创建时间

```python
# 用户数据模型
class UserModel(db.Model):
    __tablename__ = "user"
    # 添加字段 id字段 primary_key=True 表示主键 autoincrement=True 表示自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    # nullable=False 表示非空 unique=True 表示唯一
    email = db.Column(db.String(20), nullable=False, )
    join_time = db.Column(db.DateTime, default=datetime.now())

```

**校验配置 (表单数据是否按照制定的格式)**

注册表单的定义，使用了Flask-WTF库中的wtforms模块。该模块提供了一种方便的方式来定义和验证表单字段。

定义了一个名为RegisterForm的类，该类继承自wtforms.Form。RegisterForm类包含了几个字段，每个字段都有相应的验证器。

这里分别用到了 `Email` `length` ,`EqualTo`(比较两个字段是否相同).`input_required`(必须输入)

```python
import wtforms

from wtforms.validators import Email, length, EqualTo,input_required

class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    captcha = wtforms.StringField(validators=[length(min=4, max=4, message="验证码有误!")])
    username = wtforms.StringField(validators=[length(min=3, max=18, message="用户名长度有误!")])
    password = wtforms.StringField(validators=[length(min=6, max=18, message="密码长度有误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致!")])
    # 字段自定义检验
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

```

**流程:**

1. 首先定义好注册表数据模型(也就是sql里面的建表)
2. 使用wtforms下的validators 定义检查类
3. 在route视图函数里面,如果请求时GET 就返回页面,如果是POST 请求,就进行数据校验 ==> 数据存储数据库 ==> 重定向页面

**几个问题:** 

1. 每个邮箱只可以注册一次,不可以重复,如何实现

> 在进行类型校验的时候,进行一个查询数据库的操作,根据用户输入的邮箱账号进行查询,
>
> - 如果有返回,就代表数据库表里面已经存在,
> - 如果没有返回, 就代表用户第一次注册,

2. 如果判断当前用户注册的邮箱 和 填写的验证码是匹配的呢
   - 用户点击发送验证码,就会将验证码 和 当前的邮箱当作一条数据 存储邮箱检验数据模型里面(表)

> - 首先获取到用户输入的验证码
>
> - 同时获取到用户输入的邮箱号码
>
> - 然后去邮箱校验数据模型表里面进行过滤查询,看是否存在
>
>   - 存在,就代表是匹配的  -- 验证码 正确
>   - 不存在, 就代表不匹配 -- 验证码 错误
>
> - ```python
>   result = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
>   if not result:
>         raise wtforms.ValidationError("验证码错误")
>   ```

### 4.2 登录模块

思路: 

- 进行表单数据的校验 (检验类 ==> wtforms下的validators  )

- 校验通过,进行数据库查询,(基于``注册表``),

  - 数据库数据对比成功,就进行数据存储(登录表), 跳转首页
  - 数据库数据对比不成功, 就说明用户输入的账号或者密码有误

  

## 总结学习:



# flask_migrate 



flask_migrate 是一个 Flask 扩展，用于数据库迁移管理。它基于 Alembic，提供了一种简单的方法来跟踪和应用数据库模式的变化。

在开发过程中，当你对数据库模型进行更改（例如添加、修改或删除表、列等）时，flask_migrate 可以帮助你自动生成迁移脚本，并将这些脚本应用到数据库中，以保持数据库模式与代码模型的同步。

使用 flask_migrate，你可以通过命令行工具 flask db 来进行数据库迁移的操作，例如创建新的迁移脚本、应用已有的迁移脚本、回滚到先前的迁移版本等。

总之，flask_migrate 简化了数据库迁移的过程，使得在开发过程中对数据库模型进行变更变得更加方便和可控。

# flask_migrate 基本使用




- flask db init

- flask db migrate

- flask db upgrade

  这三个指令是使用 Flask-Migrate 进行数据库迁移时常用的指令，具体功能如下：

1. `flask db init`：这个指令用于初始化数据库迁移环境。它会在项目根目录中创建一个名为 `migrations` 的文件夹，用于存储数据库迁移的脚本文件。

2. `flask db migrate`：这个指令用于生成数据库迁移脚本。它会根据你对数据库模型的变更（例如添加新的表、修改表结构等）自动生成一个迁移脚本文件。这个脚本文件包含了将数据库从当前版本迁移到最新版本所需的操作。

3. `flask db upgrade`：这个指令用于执行数据库迁移。它会将数据库迁移到最新的版本，即应用最新的迁移脚本文件中定义的数据库结构。

使用这三个指令的典型流程如下：

1. 在项目根目录中运行 `flask db init`，初始化数据库迁移环境。
2. 修改数据库模型，例如添加新的表或修改表结构。
3. 运行 `flask db migrate`，生成数据库迁移脚本。
4. 运行 `flask db upgrade`，执行数据库迁移，将数据库迁移到最新版本。

这样，你就可以方便地对数据库模型进行变更，并将这些变更应用到数据库中。注意，每次修改数据库模型后都需要运行 `flask db migrate` 和 `flask db upgrade` 来生成和应用迁移脚本。