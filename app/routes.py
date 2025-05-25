from base64 import b64encode

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from models import User, GLBModel


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/sing-up", methods=['GET', 'POST'])
def singUp():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('re_password')

    if request.method == 'POST':
        if User.query.filter_by(login=login).first() is not None:
            flash('Пользователь с таким логином уже существует')
            return render_template("sing-up.html")
        if not (login or password or password2):
            flash('Пожалуйста заполните все поля')
            return render_template("sing-up.html")
        elif password != password2:
            flash("Пароли не совпадают")
            return render_template("sing-up.html")
        else:
            hashpwd = generate_password_hash(password)
            new_user = User(login=login, password=hashpwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('singIn'))

    else:
        return render_template("sing-up.html")


@app.route("/sing-in", methods=['GET', 'POST'])
def singIn():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect((url_for('index')))

        else:
            flash('Ошибка авторизации')
            return render_template("sing-in.html")
    else:

        return render_template("sing-in.html")


@app.route('/profile')
@login_required
def profile():

    return render_template('profile.html', load_user=load_user,modelDecoder=modelDecoder)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('profile.html', load_user=load_user, modelDecoder=modelDecoder)
    if request.method == 'POST':
        file = request.files['file']
        if file:
            glbmodel = file.read()
            new_model = GLBModel(userId=current_user.get_id(), model=glbmodel)
            db.session.add(new_model)
            db.session.commit()
            return render_template('profile.html', load_user=load_user,modelDecoder=modelDecoder)
        else:
            flash("Ошибка загрузки файла")
            return render_template('profile.html', load_user=load_user,modelDecoder=modelDecoder)
    else:
        return render_template('profile.html', load_user=load_user,modelDecoder=modelDecoder)
    return render_template('profile.html', load_user=load_user, modelDecoder=modelDecoder)

def load_user():
    return User.query.get(current_user.get_id())


def modelDecoder(model):
    new_model = b64encode(model).decode("utf-8")
    return new_model
