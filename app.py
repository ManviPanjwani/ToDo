from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# In-memory storage
tasks = []
task_id_counter = 1

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# POST create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    global task_id_counter

    # Try to parse the JSON body
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()

    # Ensure 'title' is included
    if 'title' not in data or not data['title']:
        return jsonify({'error': 'Title is required'}), 400

    new_task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': data.get('completed', False)
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

# PUT update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['description'] = data.get('description', task['description'])
            task['completed'] = data.get('completed', task['completed'])
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

# DELETE a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    original_len = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) < original_len:
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404

# Optional: root message
@app.route('/')
def home():
    return "To-Do List API is running! Try /api/tasks", 200

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
