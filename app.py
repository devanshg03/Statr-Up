from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_create = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():

    if Startup.query.count() < 1:
        nice = "No projects"
    else:
        rowId = Startup.query.order_by(func.random()).first().id
        nice = Startup.query.filter_by(id=rowId).first()
        nice = nice.content

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Startup(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Startup.query.order_by(Startup.date_create).all()

        return render_template('index.html', tasks=tasks, nice=nice )

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Startup.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])

def update(id):
    task = Startup.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
    
