from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # telling where the database is located
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to disable tracking
db = SQLAlchemy(app)

class Todo(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False)  

@app.route('/')
def home():
    todo_list = Todo.query.all()  
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')  # get title from form
    description = request.form.get('description')  # get description from form
    new_task = Todo(title=title, description=description, status=False)  # create new task
    db.session.add(new_task)  # new task will be added to the database
    db.session.commit()  # save changes
    return redirect(url_for('home'))

@app.route('/update/<int:todo_id>', methods=['POST'])  
def update(todo_id):
    todo = Todo.query.get(todo_id)  # return specific entry
    todo.status = not todo.status  # toggle the status of the task
    db.session.commit()  # save changes
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>', methods=['POST']) 
def delete(todo_id):
    todo = Todo.query.get(todo_id)  # return specific entry
    db.session.delete(todo)  # delete the task
    db.session.commit()  # save changes
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
