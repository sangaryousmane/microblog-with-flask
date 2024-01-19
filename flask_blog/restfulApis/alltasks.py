from tasks import tasks
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__);
auth = HTTPBasicAuth();


@app.errorhandler(404)
def page_not_found(error):
    """
    Sorry! page not found
    :return: a custom json
    """
    return make_response(jsonify({"Error": "Page Not Found"}), 404);


@app.route('/')
@app.route("/todos/v1/tasks/", methods=['GET'])
@auth.login_required
def get_all_tasks():
    """
    Get all tasks
    :return: a restful list of all tasks
    """
    return jsonify({"tasks": tasks});


# Get a single task
@app.route("/todos/v1/tasks/<int:task_id>", methods=['GET'])
def get_task(task_id: int):
    """
    Get a single task
    :param task_id:
    :return: a single task
    """
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404);
    return jsonify({"task": task[0]})


@app.route("/todos/v1/tasks", methods=['POST'])
def create_task():
    """
    Create a new task
    :return: a json of tasks
    """
    if not request.json and 'title' not in tasks:
        abort(400);
    task = {
        'id': tasks[-1]['id'] + 1, # The last id plus one(meaning a new id),
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task);
    return jsonify({"New task": task}), 201


@app.route("/todos/v1/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    """
    Deletes a task
    :param task_id:
    :return: A boolean to specify deletion
    """
    task = [task for task in tasks if tasks['id'] == task_id]
    if len(task) == 0:
        abort(404);
    tasks.remove(task[0]);
    return jsonify({"result": True})

@app.route("/todos/v1/tasks/<int:task_id>", methods=['PUT'])
def update_todos(task_id):
    """
    Updates the todo list tasks after validation
    :param task_id:
    :return: the updated task
    """
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

def make_public_task(task):
    """
    Make the URI public instead of ID
    :param task:
    :return: a new task with ID expose
    """
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@auth.get_password
def get_password(username):
    """

    :return: a user password
    """
    return 'python' if username == 'Ousmane' else None;

@app.errorhandler
def unauthorized():
    """
    User needs to be authenticated
    :return: 401 message
    """
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
