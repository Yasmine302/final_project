from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.thought import Thought

@app.route('/signin')
def signin():
    if "user_id" not in session:
        flash("Must Login!!")
        return redirect('/logout')
    user_dict = {
        'id':session['user_id']
    }
    user = User.get_by_id(user_dict)
    return render_template("signin.html", user=user )

@app.route('/signup')
def signup():
    return render_template("signup.html" )

@app.route('/home')
def thought_home():
    if "user_id" not in session:
        flash("Must Login!!")
        return redirect('/logout')
    user_dict = {
        'id':session['user_id']
    }
    user = User.get_by_id(user_dict)
    thoughts = Thought.get_all()
    return render_template("home.html", user=user, thoughts=thoughts)

@app.route('/show/thought/<thought_id>')
def thought_data(thought_id):
    if "user_id" not in session:
        flash("Must Login!!")
        return redirect('/logout')
    user_dict = {
        'id':session['user_id']
    }
    user = User.get_by_id(user_dict)
    thought = Thought.get_one_by_id(thought_id)
    return render_template('thought_data.html',thought=thought, user=user)

@app.route('/new/thought')
def create_page():
    if "user_id" not in session:
        flash("Must Login!!")
        return redirect('/logout')
    user_dict = {
        'id':session['user_id']
    }
    user = User.get_by_id(user_dict)
    return render_template("new_thought.html",user=user)

@app.route('/edit/<thought_id>')
def edit_page(thought_id):
    if "user_id" not in session:
        flash("Must Login!!")
        return redirect('/logout')
    user_dict = {
        'id':session['user_id']
    }
    user = User.get_by_id(user_dict)
    thought = Thought.get_one_by_id(thought_id)
    return render_template('edit_thought.html',thought=thought,user=user)

@app.route('/delete/<thought_id>')
def delete_thought(thought_id):
    if "user_id" not in session:
        flash("Must Login!!")
        return redirect('/logout')
    thought_dict = {
        'id' : thought_id
    }
    Thought.delete_by_id(thought_dict)
    return redirect('/home')

@app.route('/thought/create',methods=['POST'])
def create_thought():
    thought_data = {
        'user_id':session['user_id'],
        'title_show' : request.form['title_show'],
        'comment': request.form['comment'],
        'num_stars': request.form['num_stars']
    }
    if not Thought.is_valid(thought_data):
        return redirect('/new/thought')
    Thought.save(thought_data)
    return redirect('/home')

@app.route('/thought/update', methods=['POST'])
def update_thought():
    thought_data = {
        'user_id':session['user_id'],
        'id' : request.form['id'],
        'user_id':session['user_id'],
        'title_show' : request.form['title_show'],
        'comment': request.form['comment'],
        'num_stars': request.form['num_stars']
    }
    if not Thought.is_valid(thought_data):
        thought_id = request.form.get('id')
        return redirect(f'/edit/{thought_id}')
    Thought.update(thought_data)
    return redirect('/home')