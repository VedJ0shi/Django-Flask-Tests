from flask import Flask, request
import json
import dbmodels


db_filename = 'todo2.db'

app = Flask(__name__)


#SQLAlchemy setup:
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_filename}' #connecting to sqlite db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #prints SQL statements to console for debug

#initialize app:
dbmodels.models.init_app(app)
with app.app_context():
    dbmodels.models.create_all() #creates all the tables defined as model classes

#rename model classes:
Task_model = dbmodels.Task
Subtask_model = dbmodels.Subtask
Category_model = dbmodels.Category

def success_response(data, code=200):
    return json.dumps({'success':True, 'data':data}), code

def failure_response(error, code=404):
    return json.dumps({'success':False, 'error':error}), code


@app.route('/tasks/')
def get_tasks():
    return success_response([task.serialize() for task in Task_model.query.all()])

@app.route('/categories/')
def get_categories():
    return success_response([cat.serialize() for cat in Category_model.query.all()])

@app.route('/tasks/', methods=['POST'])
def create_task():
    post_body = json.loads(request.data)
    description = post_body.get('description', '')
    new_task = Task_model(description=description, done=False) #create new Task instance (new entry)
    dbmodels.models.session.add(new_task)
    dbmodels.models.session.commit()
    return success_response(new_task.serialize(), 201)

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = Task_model.query.filter_by(id=task_id).first() #returns None, if it can find the id
    if not task:
        return failure_response('Task not found')
    return success_response(task.serialize())

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task_model.query.filter_by(id=task_id).first()
    if not task:
        return failure_response('Task not found')
    put_body = json.loads(request.data)
    actions = put_body.get('actions')
    if not actions or not isinstance(actions, dict):
        return failure_response('Invalid format for PUT request')
    task.description = actions.get('description', task.description)
    task.done = actions.get('done', task.done)
    if task.done == 'True':
        task.done = True
    if task.done == 'False':
        task.done = False
    dbmodels.models.session.commit()
    return success_response(task.serialize())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task_model.query.filter_by(id=task_id).first()
    if not task:
        return failure_response('Task not found')   
    dbmodels.models.session.delete(task) #deleted from database, not local memory
    dbmodels.models.session.commit()
    return success_response(task.serialize())


@app.route('/tasks/<int:task_id>/subtask')
def get_subtasks(task_id):
    task = Task_model.query.filter_by(id=task_id).first()
    if not task:
        return failure_response('Task not found')
    subtasks = [subtask.serialize() for subtask in task.subtasks]
    return success_response(subtasks)


@app.route('/tasks/<int:task_id>/subtask', methods=['POST'])
def create_subtask(task_id):
    post_body = json.loads(request.data)
    task = Task_model.query.filter_by(id=task_id).first()
    if not task:
        return failure_response('Task not found')
    description = post_body.get('description')
    new_subtask = Subtask_model(description=description, done=False, task_id=task_id)
    dbmodels.models.session.add(new_subtask)
    dbmodels.models.session.commit()
    return success_response(new_subtask.serialize())


@app.route('/tasks/<int:task_id>/category', methods=['POST', 'PUT'])
def assign_category(task_id):
    task = Task_model.query.filter_by(id=task_id).first()
    if not task:
        return failure_response('Task not found')
    post_body = json.loads(request.data)
    description = post_body.get('description')
    if not description:
        return failure_response('No description of category provided')
    cat = Category_model.query.filter_by(description=description).first()
    if not cat:
        cat = Category_model(description=description)
    task.categories.append(cat)
    dbmodels.models.session.commit()
    return success_response(task.serialize())

if __name__ == '__main__':
    print('Registered app routes:')
    for route in app.url_map.iter_rules():  
        print(route.rule,'-->', route.endpoint)
    app.run(host='127.0.0.1', port=5000, debug=True)