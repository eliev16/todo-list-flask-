from flask import Blueprint, render_template, request, redirect, url_for, g
from todor.auth import login_required
from .models import Todo, Usuario
from todor import db


bp = Blueprint('toDo', __name__, url_prefix='/toDo')


@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos = todos)


@bp.route('/crear', methods=('GET', 'POST'))
@login_required
def crear():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo(g.user.id, title, desc)
        #Agregar tarea
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('toDo.index')) 
    return render_template('todo/crear.html')


def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo


@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    todo = get_todo(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.descripcion = request.form['descripcion']
        todo.state = True if request.form.get('state') == 'on' else False
        #editar tarea
        db.session.commit()
        return redirect(url_for('toDo.index')) 
    return render_template('todo/update.html', todo = todo)


@bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('toDo.index'))

