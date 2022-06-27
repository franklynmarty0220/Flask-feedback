from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    "Redirects to register"

    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register():
    """Shows form to register/create user """
    
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password,first_name, last_name, email)
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """ Produces Login form for Users """


    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid Username/Password"]
            return render_template("users/login.html", form=form)
    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user= User.query.get(username)
    
    delete_form = DeleteForm()

    return render_template("users/show.html", user=user, delete_form=delete_form)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Remove user"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/new", methods = ["GET", "POST"])
def new_feedback(username):
    """Show new feedback form and process it"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    feedback_form = FeedbackForm()

    if feedback_form.validate_on_submit():
        title = feedback_form.title.data
        content = feedback_form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", feedback_form=feedback_form)

@app.route("/feedback/<int: feedback_id>/update", methods= ["GET", "POST"])
def update_feedback(feedback_id):
    """Show feedback form and update """

    fb = Feedback.query.get(feedback_id)

    if "username" not in session or fb.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=fb)

    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{fb.username}")
    
    return render_template("feedback/edit.html", form=form, feedback = fb)

@app.route("/feedback/<int: feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    fb = Feedback.query.get(feedback_id)
    if "username" not in session or fb.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(fb)
        db.session.commit()
    
    return redirect(f"/users/{fb.username}")

