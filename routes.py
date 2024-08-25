from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, Task
from . import app, db

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username})
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user = get_jwt_identity()
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data['description'],
        status=data['status'],
        priority=data['priority'],
        due_date=data['due_date'],
        user_id=User.query.filter_by(username=user['username']).first().id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=User.query.filter_by(username=user['username']).first().id).all()
    return jsonify([task.as_dict() for task in tasks]), 200

@app.route('/api/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    data = request.get_json()
    task = Task.query.get(id)
    if task:
        task.title = data['title']
        task.description = data['description']
        task.status = data['status']
        task.priority = data['priority']
        task.due_date = data['due_date']
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404
