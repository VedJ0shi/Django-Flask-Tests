from flask_sqlalchemy import SQLAlchemy

models = SQLAlchemy()

join_table = models.Table(
    'association', 
    models.Column('task_id', models.Integer, models.ForeignKey('task.id')),
    models.Column('cat_id', models.Integer, models.ForeignKey('category.id')))

class Task(models.Model):
    __tablename__ = 'task'
    id = models.Column(models.Integer, primary_key=True)
    description = models.Column(models.String, nullable=False)
    done = models.Column(models.Boolean, nullable=False)
    subtasks = models.relationship('Subtask', cascade='delete', back_populates='task')
    categories = models.relationship('Category', secondary=join_table, back_populates='tasks')

    def __init__(self, **kwargs): #do not need to initialize pk (id field)
        self.description = kwargs.get('description')
        self.done = kwargs.get('done')
    
    def serialize(self):
        return {'id': self.id, 
                'description': self.description, 
                'done': self.done}


class Subtask(models.Model):
    __tablename__ = 'subtask'
    id = models.Column(models.Integer, primary_key=True)
    description = models.Column(models.String, nullable=False)
    done = models.Column(models.Boolean, nullable=False)
    task_id = models.Column(models.Integer, models.ForeignKey('task.id'))
    task = models.relationship('Task', back_populates='subtasks')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.done = kwargs.get('done')
        self.task_id = kwargs.get('task_id')

    def serialize(self):
        return {'id': self.id, 
                'description': self.description, 
                'done': self.done}


class Category(models.Model): #many-to-many relation with task
    __tablename__ = 'category'
    id = models.Column(models.Integer, primary_key=True)
    description = models.Column(models.String, nullable=False)
    tasks = models.relationship('Task', secondary=join_table, back_populates='categories')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
    
    def serialize(self):
        return {'id':self.id,
                'description':self.description}

