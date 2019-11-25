from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

@app.route('/', methods=["GET","POST"])
def add():
    if request.method == 'POST':
        try:
            task = Task(name = request.form.get('name'))
            db.session.add(task)
            db.session.commit()
        except Exception as e:
            print('Failed to add task')
            print(e)
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@app.route('/complete', methods=["POST"])
def complete():
    name = request.form.get('name')
    task = Task.query.filter_by(name=name).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route('/update', methods=["POST"])
def update():
    try:
        new_task = request.form.get('newtask')
        old_task = request.form.get('oldtask')

        task = Task.query.filter_by(name=old_task).first()
        task.name = new_task
        task.pub_date = datetime.now()
        db.session.commit()
    except Exception as e:
        print('Could not edit task name')
        print(e)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)