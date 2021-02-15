import os
import secrets
from PIL import Image
from flask import render_template, request, session, flash, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddTransactionForm
from app.models import User, Transaction
from app import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    return render_template("home.html", title = "Home Page")

@app.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), password=hashed_password, email=form.email.data.lower())
        db.session.add(user)
        db.session.commit()
        flash(f'Hi {form.username.data}, your account is created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route("/login", methods = ["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful, Check username & password','danger')
    return render_template("login.html", title = "Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    f_ext = os.path.split(form_picture.filename)[1]
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,"static","profile_pics",picture_fn)
    if current_user.image_file != "default.jpg":
        prev_pic = os.path.join(app.root_path,"static","profile_pics",current_user.image_file)
        if os.path.exists(prev_pic):
            os.remove(prev_pic)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn = save_picture(form.picture.data)
            current_user.image_file = picture_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for("static", filename="profile_pics/"+current_user.image_file)
        return render_template("account.html", title = "Account", image_file=image_file, form=form)

@app.route("/add_transaction", methods=["GET","POST"])
@login_required
def add_transaction():
    form = AddTransactionForm()
    if form.validate_on_submit():
        record = Transaction(particulars=form.particulars.data, date=form.date.data, amount=form.amount.data,
                            t_type=form.t_type.data[0], user_id=current_user.id)
        db.session.add(record)
        db.session.commit()
        flash('Your transaction has been added','success')
        return redirect(url_for('add_transaction'))
    return render_template("transact.html", title = "Add Tranaction", form=form)

@app.route("/view_transactions",methods=["GET","POST"])
@login_required
def view_transactions():
    data = Transaction.query.filter_by(user_id=current_user.id)
    return render_template("transaction.html",title="View Transactions", data = data)

