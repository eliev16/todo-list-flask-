from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
    )
from werkzeug.security import generate_password_hash, check_password_hash
from todor import db
from . import models    #importando modelos de la base de datos
from .models import Usuario


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/registro', methods = ('GET', 'POST'))
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario(username, generate_password_hash(password))
        error = None
        user_name = Usuario.query.filter_by(username = username).first()
          
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
            flash(error)
    return render_template('auth/registro.html')


@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        # Validar datos
        user = Usuario.query.filter_by(username = username).first()
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'     
        # Iniciar sesion
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('toDo.index'))
       
        flash(error)
    return render_template('auth/iniciarSesion.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.get_or_404(user_id)
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
    