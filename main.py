from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
import datetime

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'CSRFSECRETKEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

current_year = datetime.datetime.now().year


# Form
class CreateForm(FlaskForm):
    todo = StringField("Enter a task")
    add = SubmitField("Add")


# db
class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(50), nullable=False)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    todos = Todo.query.all()
    form = CreateForm()
    if form.validate_on_submit():
        todo_to_add = form.todo.data
        new_todo = Todo(todo=todo_to_add)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("index.html", form=form, todos=todos, year=current_year)


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo_to_delete = Todo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
