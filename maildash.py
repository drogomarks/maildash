from flask import Flask, jsonify, render_template, request, session, redirect, url_for, make_response, flash, abort
from flask_mail import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import CreateMailbox
from apiTool import *
from usermgmt import *
import json

app = Flask(__name__)
# For email
mail = Mail(app)

# DB Connector Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mailman:WTFpassword1***@10.209.128.62/maildash'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.secret_key = "development-key"

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    date_created = db.Column(db.String(255))
    usagemb = db.Column(db.Integer())
    usagegb = db.Column(db.Float())
    percentused = db.Column(db.Float())

    def __init__(self, username, date_created, usage):
        self.username = username
        self.date_created = date_created
        self.usagemb = usagemb
        self.usagegb = usagegb
        self.percentused = percentused


# Index view
@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect("/mailboxes")

@app.route('/login', methods=['POST'])
def do_admin_login():
    fail = "Login failed :("
    if request.form['password'] == 'Creative1!' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return index()
    else:
        return render_template("login.html", fail=fail)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

# View to get a list of mailbox users
@app.route("/mailboxes", methods=['GET'])
def get_mailboxes():
    users = User.query.all()
    data = domain_get('iccenter.org')
    max_mailboxes = data['rsEmailMaxNumberMailboxes']
    curr_mailboxes = data['rsEmailUsedStorage']
    avail_mailboxes = max_mailboxes - curr_mailboxes
    return render_template("mailboxes.html", users=users, max_mailboxes=max_mailboxes,
                                            curr_mailboxes=curr_mailboxes, avail_mailboxes=avail_mailboxes)

@app.route("/delete/<username>", methods=['GET', 'POST'])
def delete_mailbox(username):
    if request.method == 'POST':
        delete_mbx(username)
        userdel_db(username)
        worked = "BOOM!"
        users = User.query.all()

        data = domain_get('iccenter.org')
        max_mailboxes = data['rsEmailMaxNumberMailboxes']
        curr_mailboxes = data['rsEmailUsedStorage']
        avail_mailboxes = max_mailboxes - curr_mailboxes
        return render_template("mailboxes.html", users=users, username=username, worked=worked,
                                                max_mailboxes=max_mailboxes,
                                                curr_mailboxes=curr_mailboxes, avail_mailboxes=avail_mailboxes)
    else:
        return redirect("/mailboxes")

@app.route("/edit/<username>", methods=['GET', 'POST'])
def edit_mailbox(username):
    if request.method == 'POST':
        new_username = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']

        data = domain_get('iccenter.org')
        max_mailboxes = data['rsEmailMaxNumberMailboxes']
        curr_mailboxes = data['rsEmailUsedStorage']
        avail_mailboxes = max_mailboxes - curr_mailboxes


        if not password1:
            fail = "Password Change required with update!"
            return render_template("edit.html", username=username, fail=fail, max_mailboxes=max_mailboxes,
                                                curr_mailboxes=curr_mailboxes, avail_mailboxes=avail_mailboxes)

        elif password1 == password2:
            edit_mbx(username, new_username, password1)
            user_update_db(username, new_username)
            success = "Yeeeehaaawww!"
            return render_template("edit.html", success=success, username=username, new_username=new_username, password1=password1)
        else:
            user_data = user_get(username)
            curr_username = user_data['name']
            password_fail = "Bro...passwords don't match."
            return render_template("edit.html", password_fail=password_fail,
                                                curr_username=curr_username)
    elif request.method == 'GET':
        data = domain_get('iccenter.org')
        max_mailboxes = data['rsEmailMaxNumberMailboxes']
        curr_mailboxes = data['rsEmailUsedStorage']
        avail_mailboxes = max_mailboxes - curr_mailboxes

        return render_template("edit.html", username=username,
                                            max_mailboxes=max_mailboxes,
                                            curr_mailboxes=curr_mailboxes, avail_mailboxes=avail_mailboxes)


@app.route("/create", methods=['GET', 'POST'])
def create_mailbox():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        display_name = request.form['display_name']
        username = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']

        data = domain_get('iccenter.org')
        max_mailboxes = data['rsEmailMaxNumberMailboxes']
        curr_mailboxes = data['rsEmailUsedStorage']
        avail_mailboxes = max_mailboxes - curr_mailboxes

        if password1 == password2:
            add_mbx(username, password1, first_name, last_name, display_name)
            user_data = user_get(username)
            success = "SWEEEEET!"
            useradd_db(username)

            return render_template("create.html", success=success, username=username, password1=password1,
                                                  max_mailboxes=max_mailboxes, curr_mailboxes=curr_mailboxes,
                                                  avail_mailboxes=avail_mailboxes)
        else:

            password_fail = "Bro...passwords don't match."
            return render_template("create.html", password_fail=password_fail,
                                                  max_mailboxes=max_mailboxes, curr_mailboxes=curr_mailboxes,
                                                  avail_mailboxes=avail_mailboxes)

    elif request.method == "GET":

        data = domain_get('iccenter.org')
        max_mailboxes = data['rsEmailMaxNumberMailboxes']
        curr_mailboxes = data['rsEmailUsedStorage']
        avail_mailboxes = max_mailboxes - curr_mailboxes

        return render_template("create.html", max_mailboxes=max_mailboxes,
                                            curr_mailboxes=curr_mailboxes,
                                            avail_mailboxes=avail_mailboxes)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8082, debug=True)
