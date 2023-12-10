

from peewee import SqliteDatabase, Model, CharField, ForeignKeyField


db = SqliteDatabase('task_manager.db')

class Category(Model):
    name = CharField(unique=True)

    class Meta:
        database = db 

class Task(Model):
    description = CharField()
    category = ForeignKeyField(Category, backref='tasks')

    class Meta:
        database = db

def initialize_database():
    # Connect to the database
    db.connect()

    # Create tables
    db.create_tables([Category, Task], safe=True)

    # Insert some initial data
    if Category.select().count() == 0:
        work_category = Category.create(name='Work')
        personal_category = Category.create(name='Personal')

        Task.create(description='Finish project', category=work_category)
        Task.create(description='Buy groceries', category=personal_category)
  