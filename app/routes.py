from app.models import User, Article, Blog, Comment
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import desc, or_, func
from .models import db, app
from flask_login import login_user, logout_user, current_user
from .forms import BlogLoginForm, BlogRegisterForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET', 'POST'])
def index():
    form = BlogLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(login=username).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('showblogs'))
            else:
                error = "密码错误"
                return render_template('index.html', error=error)
        else:
            error = "用户不存在"
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = BlogRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        login = request.form['login']
        password = request.form['password']
        email = request.form['email']
        userc = User.query.filter_by(login=login).count()
        if userc == 0:
            user = User(login=login, password=generate_password_hash(password), email=email)
            db.session.add(user)
            db.session.commit()
            return render_template("index.html")
        else:
            error = "名称已存在"
            return render_template("register.html", error=error)
    else:
        return render_template('register.html')

@app.route('/showblogs')
def showblogs():
    blogs = Blog.query.order_by(desc('id')).all()
    return render_template('showblogs.html', blog=blogs)

@app.route('/addblog', methods=['GET', 'POST'])
def addblog():
    if request.method == 'GET':
        return render_template('addblog.html')
    else:
        title = request.form['title'].replace("\'", "\"")
        content = request.form['content'].replace("\'", "\"")
        blog = Blog(title=title, content=content)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('showblogs'))

@app.route('/details<int:id>', methods=['GET', 'POST'])
def details(id):
    if request.method == 'GET':
        blog = Blog.query.get(id)
        comment = Comment.query.filter(Comment.blog_id==id).order_by(desc('datetime'  ))
        commt = {}
        for com in comment:
            a = str(com.datetime).rsplit('.', 1)[0] # 直接用split处理时间字段
            commt[a] = com.comment
        return render_template('details.html', blog=blog, comments=commt)
    else:
        comment = request.form['comment'].replace("\'", "\"")
        comment = Comment(comment=comment, blog_id=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('details', id=id))

@app.route('/editblogs')
def edit():
    blogs = Blog.query.order_by(desc('id')).all()
    return render_template('editblog.html', blog=blogs)


@app.route('/edit<int:id>', methods=['GET', 'POST'])
def editblog(id):
    if request.method == 'GET':
        blog = Blog.query.get(id)
        title = blog.title
        content = blog.content
        return render_template('editdetail.html', title=title, content=content, id=id)
    else:
        title = request.form['title']
        content = request.form['content']
        id = request.form['id']
        blog = Blog.query.get(id)
        blog.title = title
        blog.content = content
        db.session.commit()
        return redirect(url_for('details', id=id))

# @app.route('/deleteblogs')
# def deleteblogs():
#     blogs = Blog.query.order_by(desc('id')).all()
#     return render_template('deleteblog.html', blog=blogs)


@app.route('/delete<id>', methods=['GET', 'POST'])
def deleteblog(id):
    if request.method == 'POST':
        id = request.form['id']
        blog = Blog.query.get(id)
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for('showblogs'))
    else:
        return redirect(url_for('details', id=id))

@app.route('/search')
def search():
    q = request.args.get('q', '')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render_template('results.html', error_msg=error_msg)
    title = Blog.query.filter(or_(func.lower(Blog.title).like('%'+func.lower(q)+'%'), func.lower(Blog.content).like('%'+func.lower(q)+'%'))).order_by(desc('id')).all()
    if len(title) == 0:
        error_msg = "查询无果"
        return render_template('results.html', error_msg=error_msg)
    return render_template('results.html', title=title)