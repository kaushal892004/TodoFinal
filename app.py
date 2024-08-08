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
# @app.route('/',methods = ['GET','POST'])
# def hello_world():
#     if request.method == 'POST':
#         title = request.form['title']
#         Desc = request.form['Desc']
#         Todo = ToDoWebApp(title = title , Desc = Desc)
#         db.session.add(Todo)
#         db.session.commit()
#     alltodo = ToDoWebApp.query.all()
#     # print(alltodo)
#     return render_template('index.html',alltodo = alltodo)
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            Desc = request.form.get('Desc')

            # Validate input data
            if not title or not Desc:
                return "Title and Description are required!", 400

            Todo = ToDoWebApp(title=title, Desc=Desc)
            db.session.add(Todo)
            db.session.commit()

        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            return f"An error occurred: {str(e)}", 500

    try:
        alltodo = ToDoWebApp.query.all()
    except Exception as e:
        return f"An error occurred while fetching data: {str(e)}", 500

    return render_template('index.html', alltodo=alltodo)


# Define the route for the hello page
@app.route('/show')
def show():
    alltodo = ToDoWebApp.query.all()
    # print(alltodo)
    return 'Hello, User'

# @app.route('/update/<int:sno>',methods = ['GET','POST'])
# def update(sno):
#     if request.method == 'POST':
#         title = request.form['title']
#         Desc = request.form['Desc']
#         ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
#         ToDo.title = title
#         ToDo.Desc = Desc
#         db.session.add(ToDo)
#         db.session.commit()
#         return redirect('/')

#     ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
#     return render_template('update.html',ToDo=ToDo) 
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    try:
        if request.method == 'POST':
            title = request.form['title']
            Desc = request.form['Desc']
            ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
            if ToDo:
                ToDo.title = title
                ToDo.Desc = Desc
                db.session.add(ToDo)
                db.session.commit()
                return redirect('/')
            else:
                return "ToDo item not found", 404

        ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
        return render_template('update.html', ToDo=ToDo)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# @app.route('/delete/<int:sno>')
# def delete(sno):
#     ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
#     db.session.delete(ToDo)
#     db.session.commit()
#     return redirect('/')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')

# # Run the Flask app
# if __name__ == "__main__":
#     # app.run(host="0.0.0.0",debug = True,port=int(os.environ.get("PORT", 5000)))
#     app.run(debug=False,port=5000)


@app.route('/delete/<int:sno>', methods=['POST'])
def delete(sno):
    try:
        ToDo = ToDoWebApp.query.filter_by(sno=sno).first()
        if ToDo:
            db.session.delete(ToDo)
            db.session.commit()
            return redirect('/')
        else:
            return "ToDo item not found.", 404
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return f"An error occurred: {str(e)}", 500

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        return f"An error occurred while rendering the page: {str(e)}", 500

@app.route('/home')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        return f"An error occurred while rendering the page: {str(e)}", 500

# Run the Flask app
if __name__ == "__main__":
    # Run with host "0.0.0.0" for public accessibility and with debug=False for production
    app.run(host="0.0.0.0", debug=False, port=int(os.environ.get("PORT", 5000)))

