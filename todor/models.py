from todor import db



class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False) 
 
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    
    def __repr__(self):
        return f'<Usuario: {self.username} >'
    
    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_by = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    title = db.Column(db.String(100), nullable = False) 
    descripcion = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)
    
    
    def __init__(self, created_by, title, descripcion, state = False):
        self.created_by = created_by
        self.title = title
        self.descripcion = descripcion
        self.state = state
        
    
    def __repr__(self):
        return f'<Todo: {self.title} >'