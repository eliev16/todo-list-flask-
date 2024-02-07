# Agregar configuraciones del proyecto
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()   # Objeto de la extension

def crear_app():
    
    app = Flask(__name__)

    # Configuracion del proyecto
    app.config.from_mapping(
        DEBUG = False,
        SECRET_KEY = 'devtodo',
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"    # Conectar la extension a flask
    )
    
    db.init_app(app)    # inicializando el SQLAlchemy
    
    # Registro de Blueprint
    from . import todo
    app.register_blueprint(todo.bp)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    
    # Migrar modelo a la base de datos
    with app.app_context():
        db.create_all()
    
    return app

