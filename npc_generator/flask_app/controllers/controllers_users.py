from flask_app import app, bcrypt
from flask import render_template, redirect, session, request

from flask_app.models import model_users

@app.route('/user/login', methods=['POST'])
def user_new():
    model_users.User.validate_login(request.form)
    # if 'remember_me' in request.form:
    #     session['email'] = request.form['email']
    # else:
    #     del session['email']
    return redirect('/')

@app.route('/user/logout')
def user_logout():
    del session['uuid']
    return redirect('/')


@app.route('/user/create', methods=['POST'])
def user_create():
    if not model_users.User.validate(request.form):
        return redirect('/')

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])

    data = {
        **request.form,
        'pw': hash_pw
    }

    user_id = model_users.User.create(data)
    session['uuid'] = user_id
    return redirect('/')

@app.route('/user/<int:id>')
def user_show(id):
    return render_template('user_show.html')

@app.route('/user/<int:id>/edit')
def user_edit(id):
    return render_template('user_edit.html')

@app.route('/user/<int:id>/update', methods=['POST'])
def user_update(id):
    return redirect('/')

@app.route('/user/<int:id>/delete')
def user_delete(id):
    return redirect('/')
