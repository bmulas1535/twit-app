from flask import render_template, flash, redirect, url_for, request
from twitapp import app, db, bcrypt
from flask_login import login_user, login_required, current_user, logout_user
from twitapp.forms import Registration, Login
from twitapp.models import User, Tuser, Tweets
from twitapp.twitter import add_or_update_user
from twitapp.predict import predict_user


@app.route('/')
def home():
    tusers = Tuser.query.all()
    return render_template("home.html", title='Home', tusers=tusers)


@app.route('/about')
def about():
    return render_template("about.html", title="About Twitoff")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Set route for register form"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {}.".format(form.username.data), "success")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            return redirect(url_for('home'))

        else:
            return redirect(url_for('login'))
    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/user', methods=['POST'])
@app.route('/user/<name>', methods=['GET'])
@login_required
def user(name=None, message=''):
    name = name or request.values['user_name']

    try:
        if request.method == 'POST':
            add_or_update_user(name)
            message = "User {} successfully added!".format(name)
        tweets = Tuser.query.filter(Tuser.name == name).one().tweets

    except Exception as e:
        message = "Error adding {}: {}".format(name, e)
        tweets = []
    return render_template('user.html', title=name, tweets=tweets,
                           message=message)


@app.route('/compare', methods=['POST'])
@login_required
def compare(message=''):
    user1, user2 = sorted([request.values['user1'],
                          request.values['user2']])
    if user1 == user2:
        message = 'Cannot compare a user to themselves!'

    else:
        prediction = predict_user(user1, user2, request.values['tweet_text'])
        message = '"{}" is more likely to be said by {} than {}'.format(
            request.values['tweet_text'], user1 if prediction else user2,
            user2 if prediction else user1)

    return render_template('prediction.html', title='Prediction',
                           message=message)


@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return render_template('home.html', title='DB Reset', users=[])
