from flask import Blueprint, render_template, request, redirect, url_for, g

# 导入数据库
from exts import db
# 导入问题模型(也可以叫做导入表)
from models import QuestionsModel, AnswerModel
# 导入表单验证
from .forms import Questions, Answers

from decorator import login_required


bp = Blueprint("Qa", __name__, url_prefix="/")


# 首页展示
@bp.route('/')
def index():
    # 访问数据库 拿数据
    questions = QuestionsModel.query.order_by(QuestionsModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


# 发送问题
@bp.route('/publish_qa', methods=['GET', 'POST'])
@login_required
def publish_qa():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = Questions(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionsModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("Qa.index"))
        else:
            print(form.errors)
            return redirect(url_for("Qa.publish_qa"))


# 查看详情
@bp.route('/qa/detail/<question_id>')
def qa_detail(question_id):
    question = QuestionsModel.query.get(question_id)
    return render_template("detail.html", question=question)


# 问题回答

@bp.route("/answer/publish", methods=["POST"])
@login_required
def publish_answer():
    form = Answers(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("Qa.qa_detail", question_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("Qa.qa_detail", question_id=request.form.get("question_id")))


# 数据库查询

@bp.route("/qa/search")
def search():
    # /qa/search?q = flask
    # /qa/search/<q>
    # post,request.form
    # 获取参数
    q = request.args.get("q")
    # 从数据库里面进行模糊查找,然后返回所有标题包含q这个标题的数据
    questions = QuestionsModel.query.filter(QuestionsModel.title.like("%" + q + "%")).all()
    # questions = QuestionsModel.query.filter(QuestionsModel.title.contains(q)).all()

    return render_template("index.html", questions=questions, q=q)



