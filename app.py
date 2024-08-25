from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20), nullable=True)

# Ensure the tables are created
with app.app_context():
    db.create_all()

# Route to get all tasks
@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        output = []

        for task in tasks:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'due_date': task.due_date
            }
            output.append(task_data)

        return jsonify({'tasks': output})
    
    elif request.method == 'POST':
        data = request.get_json()

        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data['status'],
            priority=data['priority'],
            due_date=data.get('due_date')
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task created successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# db = SQLAlchemy(app)

# # Task model
# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(200), nullable=True)
#     status = db.Column(db.String(20), nullable=False)
#     priority = db.Column(db.String(20), nullable=False)
#     due_date = db.Column(db.String(20), nullable=True)

# # Ensure the tables are created
# with app.app_context():
#     db.create_all()

# # Route to get all tasks
# @app.route('/api/tasks', methods=['GET'])
# def get_tasks():
#     tasks = Task.query.all()
#     output = []

#     for task in tasks:
#         task_data = {
#             'id': task.id,
#             'title': task.title,
#             'description': task.description,
#             'status': task.status,
#             'priority': task.priority,
#             'due_date': task.due_date
#         }
#         output.append(task_data)

#     return jsonify({'tasks': output})

# if __name__ == '__main__':
#     app.run(debug=True)

