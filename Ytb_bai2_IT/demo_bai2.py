import os

from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy  import SQLAlchemy
from os import path
from flask_mail import Mail, Message
app = Flask(__name__)
app.config["SECRET_KEY"]="LDVNLSNVL"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:hieu26082001@localhost/csdl2_ytb_thanh_it?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app=app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME']='cubin26082001@gmail.com'
app.config['MAIL_PASSWORD']='sbifkgoeiqhkquhn'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/ok')
def home():
    return render_template("layout/home.html")

@app.route('/login', methods=["POST", "GET"])
def login_hello():
    if request.method == "POST":
        user_name = request.form["name"]
        session.permanent = True
        if user_name:
            session["user"] = user_name
            found_user = User.query.filter_by(name = user_name).first()
            if found_user:
                session["email"] = found_user.email

            else:
                user = User(user_name, "temp@gmail.com")
                db.session.add(user)
                db.session.commit()
            flash("Ban da login databate thanh cong","info")
            # return render_template("layout/user.html", user=user_name)
            return redirect(url_for("user", user=user_name))


    if "user" in session:
        name = session["user"]
        flash("Ban da login", "info")
        # return render_template("layout/user.html", user=name)
        return redirect(url_for("user", user=name))
    return render_template("layout/login.html")


@app.route('/forget', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        msg = Message("ok man", sender='noreply@demo.com',
                      recipients=['hieukato321@mail.com'])
        msg.body = "Hey how are you ? OK nha"
        mail.send(msg)
        return "DA GUI"

    return render_template("layout/forget.html")

@app.route('/reset')
def reset():
    return render_template("layout/resetpass.html")


@app.route('/hoa')
def hello_admin():
    return render_template("layout/admin.html", text="XIN CHAO co admin", cars = ['xe may','honda','xe dap'])

# @app.route("/user/<name>")
# def hello_user(name):
#     if name == 'admin':
#         return redirect(url_for('hello_admin'))
#     return render_template("demo2.html", massage="XIN CHAO %s !!" % name)


@app.route("/user", methods = ['get', 'post'])
def user():
    email = None
    if "user" in session:
        name = session["user"]
        if request.method == "POST":
            if not request.form["email"] and request.form["name"]:
                User.query.filter_by(name = name).delete()
                db.session.commit()
                flash("ban da xoa user")
                return redirect(url_for("hello_logout"))
            else:
                email = request.form["email"]
                session["email"] = email
                found_user = User.query.filter_by(name = name).first()
                found_user.email = email
                db.session.commit()
                flash("email da duoc sua doi")
        elif "email" in session:
            email = session["email"]
        return render_template("layout/user.html", user= name, email = email)
    else:
        flash("Ban chua login", "info")
        # return render_template("demo2.html", massage="XIN CHAO %s !!" % name)
        return redirect(url_for("login_hello"))


@app.route('/logout')
def hello_logout():
    flash("Ban da logout thanh cong", "info")
    session.pop("user", None)
    return redirect(url_for("login_hello"))


if __name__ == "__main__":
    if not path.exists("user.db"):
        # db.create_all(app=app)
         print("Created database")
    app.run(debug=True)