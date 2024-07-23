from flask import Flask, request
import json
import dbinterface

driver = dbinterface.DatabaseDriver()

app = Flask(__name__)   #Flask Application instance


def success_response(data, code=200):
    return json.dumps({'success':True, 'data':data}), code

def failure_response(error, code=404):
    return json.dumps({'success':False, 'error':error}), code


#each of the below endpoints/functions performs a database operation and returns an HTTP response:
@app.route('/tasks/')
def get_tasks():
    return success_response(driver.get_all_tasks())


@app.route('/tasks/', methods=['POST'])
def create_task():
    post_body = json.loads(request.data)
    description = post_body.get('description')
    if description:
        new_id = driver.insert_task(description)
        return success_response(driver.get_task_by_id(new_id), 201)
    return failure_response('No task description provided', 400)

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = driver.get_task_by_id(task_id)
    if task:
        return success_response(task)
    return failure_response('Task not found')
    
    
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = driver.get_task_by_id(task_id)
    if not task:
        return failure_response('Task not found')
    put_body = json.loads(request.data)
    actions = put_body.get('actions')
    if not actions or not isinstance(actions, dict):
        return failure_response('Invalid format for PUT request')
    driver.update_task_by_id(task_id, **actions)
    return success_response(driver.get_task_by_id(task_id))



@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = driver.get_task_by_id(task_id)
    if not task:
        return failure_response('Task not found')
    driver.delete_task_by_id(task_id)
    return success_response(task)


@app.route('/tasks/<int:task_id>/subtask')
def get_subtasks(task_id):
    task = driver.get_task_by_id(task_id)
    if not task:
        return failure_response('Task not found')
    return success_response(driver.get_subtasks_of_task(task_id))


@app.route('/tasks/<int:task_id>/subtask', methods=['POST'])
def create_subtask(task_id):
    post_body = json.loads(request.data)
    task = driver.get_task_by_id(task_id)
    if not task:
        return failure_response('Task not found')
    description = post_body.get('description')
    new_id = driver.insert_subtask(description, task_id)
    return success_response(driver.get_subtask_by_id(new_id))



if __name__ == '__main__':
    print('Registered app routes:')
    for route in app.url_map.iter_rules():  
        print(route.rule,'-->', route.endpoint)
    app.run(host='0.0.0.0', port=5000, debug=True)