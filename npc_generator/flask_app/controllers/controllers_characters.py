from flask_app import app
from flask import render_template, redirect, session, request

from flask_app.models import model_characters, model_users

@app.route('/character/new')
def character_new():
    context = {
    'user': model_users.User.get_one({'id': session['uuid']})
    }
    return render_template('new_character.html', **context)

@app.route('/character/create', methods=['POST'])
def character_create():
    if not model_characters.Character.validate(request.form):
        return redirect('/character/new')

    data = {
        **request.form,
        'user_id': session['uuid']
    }
    print(data)
    id = model_characters.Character.create(data)
    print(id)
    return redirect('/')

@app.route('/character/<int:id>') 
def character_show(id):
    context = {
    'user': model_users.User.get_one({'id': session['uuid']}),
    'character': model_characters.Character.get_one({'id':id})
    }
    return render_template('show_character.html', **context)

@app.route('/character/<int:id>/edit')
def character_edit(id):
    context = {
    'user': model_users.User.get_one({'id': session['uuid']}),
    'character': model_characters.Character.get_one({'id':id})
    }
    return render_template('edit_character.html', **context)

@app.route('/character/<int:id>/update', methods=['POST'])
def character_update(id):
    if not model_characters.Character.validate(request.form):
        return redirect(f'/character/{id}/edit')
    data = {
        **request.form,
        'id' : id
    }
    model_characters.Character.update_one(data)
    return redirect('/')


@app.route('/character/<int:id>/delete')
def character_delete(id):
    model_characters.Character.delete_one({'id': id})
    return redirect('/dashboard')

@app.route('/character/<int:id>/view')
def character_view(id):
    return redirect('/character/<int:id>')
