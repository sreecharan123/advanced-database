from bottle import Bottle, template, redirect, request
from database import initialize_database, Category, Task

app = Bottle()

# Initialize the database
initialize_database()

@app.route("/")
def get_index():
    return redirect("/list")

@app.route("/list", method="GET")
def get_list_tasks():
    category_id = request.query.get("category")

    if category_id:
        tasks = Task.select(Task, Category).join(Category).where(Category.id == category_id)
    else:
        tasks = Task.select(Task, Category).join(Category)

    categories = Category.select()  # Include all categories for the dropdown
    return template("list_tasks.html", task_list=tasks, category_list=categories)

@app.route("/list_categories")
def get_list_categories():
    categories = Category.select()
    return template("list_categories.html", category_list=categories)

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

@app.route("/update/<id:int>", method="GET")
def get_update(id):
    task = Task.get(Task.id == id)
    categories = Category.select()
    return template("update_task.html", task=task, categories=categories)

@app.route("/update/<id:int>", method="POST")
def post_update(id):
    description = request.forms.get("description")
    category_id = request.forms.get("category")
    Task.update(description=description, category=category_id).where(Task.id == id).execute()
    return redirect("/list")

@app.route("/delete/<id:int>")
def get_delete(id):
    task = Task.get(Task.id == id)
    task.delete_instance()
    return redirect("/list")
@app.route("/add_category", method="GET")
def get_add_category():
    return template("add_category.html")

@app.route("/add_category", method="POST")
def post_add_category():
    name = request.forms.get("name")
    Category.create(name=name)
    return redirect("/list_categories")


@app.route("/update_category/<category_id:int>", method="GET")
def get_update_category(category_id):
    category = Category.get(Category.id == category_id)
    return template("update_category.html", category=category)

@app.route("/update_category/<category_id:int>", method="POST")
def post_update_category(category_id):
    new_name = request.forms.get("name")
    Category.update(name=new_name).where(Category.id == category_id).execute()
    return redirect("/list_categories")

@app.route("/delete_category/<category_id>")
def get_delete_category(category_id):
    category = Category.get(Category.id == category_id)
    category.delete_instance()
    return redirect("/list_categories")
if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
