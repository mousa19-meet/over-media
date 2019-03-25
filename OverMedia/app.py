from flask import Flask, flash, render_template, url_for, redirect, request, session as flask_session
from Database import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home():
    posts = query_all_posts() 
    posts = posts[::-1]

    if 'username' in flask_session:
        user_name = flask_session['username']
        status = query_user_by_name(user_name).status
        return render_template('home_loggedin.html',name="logged in as : " + user_name ,status= status ,posts=posts)
    else :
        return render_template('home.html',posts=posts)

@app.route('/quiz', methods=["GET","POST"])
def quiz():
    if 'username' in flask_session:
        user_name = flask_session['username']
        if request.method == "GET":
            return render_template('quiz.html')
        else:
            number1 = request.form["Q1"]
            number2 = request.form["Q2"]
            number3 = request.form["Q3"]
            number4 = request.form["Q4"]
            number5 = request.form["Q5"]
            number6 = request.form["Q6"]
            total = int(number1) + int(number2) + int(number3) + int(number4) + int(number5) + int(number6)
            if total <= 9:
                update_User(user_name,"Free of media")
            elif total <= 13:
                update_User(user_name,"Using but living")
            elif total <= 16:
                update_User(user_name,"Caring to share")
            elif total <= 20:
                update_User(user_name,"Mildly addicted")
            elif total <= 25:
                update_User(user_name,"Friends come and go, but likes stay Forever")
            else:
                update_User(user_name,'Ultra Addicted')

            return redirect(url_for('home'))
    else:
        return redirect(url_for('log_in'))

@app.route('/create-tip',methods=['GET','POST'])
def create_tip(): 
    if 'username' in flask_session:
        if request.method == 'GET':
            return render_template('tips.html')
        else:
            tip_string = request.form['tip_submit']
            add_Post(tip_string)
            return redirect(url_for('home'))
    else:
        return redirect(url_for('log_in'))

@app.route('/log-in', methods=['GET','POST'])
def log_in():
    if request.method == 'POST':
        name = request.form['uname']
        password = request.form['psw']
        posts = query_all_posts()
        posts = posts.reverse()
        user = query_by_name_and_password(name, password)

        if user is not None and user.password == password:
            flask_session['username'] = user.name
            return redirect(url_for('home'))
        else :
            error = 'Username & Password do not match , Please try again'
            flash(error)
            return render_template('log_in.html')
    else:       
        return render_template('log_in.html')

@app.route('/log-out')
def log_out():
    posts = query_all_posts()
    posts = posts[::-1]

    if 'username' in flask_session:
        del flask_session['username']
        return render_template('home.html',name="",posts=posts)
    else:
        return redirect(url_for('home'))

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['username'] 
        password = request.form['psw']
        status = 'new'
        if query_user_by_name(name) == None:
            add_User(name,password,status)
            flash('You were successfully signed up')
            return redirect(url_for('log_in'))
        else:
            flash('Username already taken, please try another one.')
            return render_template('sign_up.html')

    else:
        return render_template('sign_up.html')

if __name__ == "__main__":
    app.run(debug=True)
