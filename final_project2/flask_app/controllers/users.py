from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/signup')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/login',methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user_db = User.get_by_email(data)
    
    if not user_db:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password,request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    
    session['user_id'] = user_db.id
    return redirect('/home')
#stuck on password implementing in this page
@app.route('/account/<user_id>')
def user_data(user_id):
    user_dict = {
        'id':session['user_id']
    }
    user = User.get_by_id(user_dict)
    return render_template('user_data.html', user=user)
#Didnt finish this part
#@app.route('/account/edit/<user_id>')
#def edit_user(user_id):
    #if "user_id" not in session:
        #flash("Must Login!!")
        #return redirect('/logout')
    #user = User.get_by_id(user_id)
    #user.email = request.form['email']
    #return render_template('user_update.html',user=user)

#@app.route('/user/update', methods=['POST'])
#def update_user():
    #user_data = {
        #'id' : request.form['id'],
        #'first_name' : request.form['first_name'],
        #'last_name': request.form['last_name'],
        #'email': request.form['email'],
        #'password': request.form['password']
    #}
    #if not User.validate_register(user_data):
        #user_id = request.form.get('id')
        #return redirect(f'/user/edit/{user_id}')
    #User.update(user_data)
    #return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')