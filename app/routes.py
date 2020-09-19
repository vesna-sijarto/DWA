from flask import render_template, flash, redirect, url_for,request
from app import app,db
from app.forms import TodoForm,LoginForm,RegistrationForm
from app.models import Todo
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user,login_required
from werkzeug.urls import url_parse



@app.route('/')
@app.route('/index',methods=['GET', 'POST'])
@login_required
def index():
    form = TodoForm()
    todo = Todo.query.all()
    if form.validate_on_submit():
        dodaj = Todo(task=form.task.data,complite=False)
        db.session.add(dodaj)
        db.session.commit()
        flash('dodali ste  novi task')
        return redirect(url_for('index'))    
    return render_template('index.html', title='Todo', form=form, todo=todo)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Create', form=form)


@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.complite= not todo.complite
    db.session.commit()
    return redirect ('/index')
    
@app.route('/delete/<int:id>',methods=['GET', 'POST'])
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect ('/index')

