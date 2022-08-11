from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import model_characters, model_users

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')

    context = {
        'user': model_users.User.get_one({'id': session['uuid']}),
        'character': model_characters.Character.get_all()
    }
    return render_template('dashboard.html', **context)

@app.route('/character/new')
def new():
    return redirect('/')