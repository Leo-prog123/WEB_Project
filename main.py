from flask import Flask, render_template, redirect, request, abort
from forms.loginform import LoginForm
from data import db_session
from data.users import User
from data.works import Works
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.works import WorksForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    works = sorted(db_sess.query(Works), key=lambda x: (not (x.is_close), x.created_date))
    return render_template("index.html", works=works)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/works', methods=['GET', 'POST'])
@login_required
def add_works():
    form = WorksForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        works = Works()
        works.time = form.time.data
        works.address = form.address.data
        works.mph = form.mph.data
        works.min_pay = form.min_pay.data
        works.amount = form.amount.data
        works.description = form.description.data
        works.ready = ''
        works.free = form.amount.data
        works.is_close = False
        current_user.works.append(works)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('works.html', title='Создание заявки',
                           form=form)


@app.route('/works/<int:id>', methods=['GET', 'POST'])
@login_required
def close_works(id):
    db_sess = db_session.create_session()
    works = db_sess.query(Works).filter(Works.id == id, Works.user != current_user).first()
    if works:
        if f'{current_user.id}|{current_user.name}|{current_user.phone}' not in works.ready:
            works.ready = works.ready + f'{current_user.id}|{current_user.name}|{current_user.phone}:'
            if works.free > 0:
                works.free = works.free - 1
            else:
                return redirect('/')
            db_sess.commit()
            return redirect('/')
        else:
            return redirect('/')
    else:
        works = db_sess.query(Works).filter(Works.id == id, Works.user == current_user).first()
        if works:
            works.is_close = True
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)


@app.route('/works_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def works_delete(id):
    db_sess = db_session.create_session()
    works = db_sess.query(Works).filter(Works.id == id,
                                        Works.user == current_user
                                        ).first()
    if works:
        db_sess.delete(works)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/delete_worker/<int:userid>/<int:workid>')
def delete_worker(userid, workid):
    db_sess = db_session.create_session()
    works = db_sess.query(Works).filter(Works.id == workid,
                                        Works.user == current_user
                                        ).first()
    new_ready_list = ''
    for worker in works.ready.split(':')[:-1]:
        if int(worker.split('|')[0]) != userid:
            new_ready_list = new_ready_list + worker + ':'
    works.ready = new_ready_list
    works.free += 1
    db_sess.commit()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/data.db")
    # db_sess = db_session.create_session()
    # user = User()
    # user.name = "Леонид"
    # user.phone = "89871565504"
    # user.email = "email@email.ru"
    # db_sess.add(user)
    # db_sess.commit()
    # works = Works(time="Сегодня 9:00", mph=400, min_pay=2, ready='', description='Перевезти 2 шкафа', amount=2, free=2, user_id=1)
    # db_sess.add(works)
    # db_sess.commit()
    # works = Works(time="Завтра 11:00", mph=350, min_pay=2, ready='', description='Офисный переезд', amount=4, free=2, user_id=1)
    # db_sess.add(works)
    # db_sess.commit()
    app.run(port=8080, host='127.0.0.1')
