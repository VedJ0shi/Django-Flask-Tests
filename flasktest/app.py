#simulating web client communicating to our server via JSON messages
from flask import Flask, request
import json

app = Flask(__name__)   #Flask Application instance

tasks = {
    0: {
        'id': 0,
        'description': 'walk Spock',
        'done': False       
    },
    1: {
        'id': 1,
        'description': 'homework',
        'done': False
    }
} #non-persisting data store


@app.route('/tasks/')
def get_tasks():
    res = {
        'success': True,
        'data': list(tasks.values())
    }
    return json.dumps(res), 200


@app.route('/tasks/', methods=['POST'])
def create_task():
    task_id = max(tasks) + 1 #max(dic) returns its greatest key
    post_body = json.loads(request.data)
    description = post_body.get('description', None) #gets the value from dic post_body
    task = {'id': task_id,
        'description': description,
        'done': False } #establishes new task
    tasks[task_id] = task #saves new task
    return json.dumps({'success': True, 'data': task}), 201  #object created and saved to 'tasks' on server-side
    
    
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found'}), 404
    put_body = json.loads(request.data)
    actions = put_body.get('actions', None)
    updates = []
    if not actions:
        return json.dumps({'success': True, 'update': None, 'data': tasks[task_id]}), 200
    if actions.get('update-description'):
        tasks[task_id]['description'] = actions.get('update-description')
        updates.append('description')
    if actions.get('update-done'):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        updates.append('done')
    return json.dumps({'success': True, 'update': updates, 'data': tasks[task_id]}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({'success': False, 'error': 'Task not found'}), 404
    del tasks[task_id]
    return json.dumps({'success': True, 'data': list(tasks.values())}), 200


@app.route('/hello/')
def hello():
    return 'Hello world'


if __name__ == '__main__':
    print('Registered routes:')
    for route in app.url_map.iter_rules():  #url_map attribute is an instance of werkzeug.routing.Map (server routing map)
        print(route.rule,'-->', route.endpoint)
    app.run(host='127.0.0.1', port=5000, debug=True)