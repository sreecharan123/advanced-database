from bottle import Bottle, template, redirect, request
from database import initialize_database, Category, Task

app = Bottle()

# Initialize the database
initialize_database()

@app.route("/")
def get_index():
    return redirect("/list")

@app.route("/list")
def get_list():
    tasks = Task.select()
    return template("list.html", task_list=tasks)

@app.route("/add", method="GET")
def get_add():
    categories = Category.select()
    return template("add_task.html", categories=categories)

@app.route("/add", method="POST")
def post_add():
    description = request.forms.get("description")
    category_id = request.forms.get("category")
    Task.create(description=description, category=category_id)
    return redirect("/list")

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
