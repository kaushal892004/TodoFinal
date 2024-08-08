from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Create the Flask application instance
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDoWebApp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define the ToDoWebApp model
class ToDoWebApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    Desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create the database tables
with app.app_context():
    db.create_all()

# Define the route for the home page
@app.route('/',methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        Desc = request.form['Desc']
        Todo = ToDoWebApp(title = title , Desc = Desc)
        db.session.add(Todo)
        db.session.commit()
    alltodo = ToDoWebApp.query.all()
    # print(alltodo)
    return render_template('index.html',alltodo = alltodo)

# Define the route for the hello page
@app.route('/show')
def show():
    alltodo = ToDoWebApp.query.all()
    # print(alltodo)
    return 'Hello, User'

@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        Desc = request.form['Desc']
        ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
        ToDo.title = title
        ToDo.Desc = Desc
        db.session.add(ToDo)
        db.session.commit()
        return redirect('/')

    ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
    return render_template('update.html',ToDo=ToDo) 

@app.route('/delete/<int:sno>')
def delete(sno):
    ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
    db.session.delete(ToDo)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Run the Flask app
if __name__ == "__main__":
    # app.run(host="0.0.0.0",debug = True,port=int(os.environ.get("PORT", 5000)))
    app.run(debug=True,port=5000)

