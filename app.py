from flask import Flask, jsonify, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# tasks -> id integer, do text, status integer, created_at text, updated_at text 

class Database():
    def __init__(self):
        self.db_name = "task.db"
        self.connect = sqlite3.connect(self.db_name)
        self.task_number =  self.count()

    def count(self):
        query = "SELECT COUNT(*) FROM tasks"
        result = self.connect.cursor().execute(query).fetchall()
        return int(result[0][0])

    def search_id(self):
        query = "SELECT id FROM tasks ORDER BY id DESC LIMIT 1"
        result = self.connect.cursor().execute(query).fetchall()
        return int(result[0][0])

    def show(self):
        query = "SELECT * FROM tasks"
        result = self.connect.cursor().execute(query).fetchall()
        self.connect.close()
        return jsonify({"tasks": result})

    def new(self, do):
        if self.task_number == 0:
            task_id = 1
        else :
            task_id = self.search_id() + 1
        dt= datetime.datetime.now()
        strdt = dt.strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO tasks VALUES ( {}, '{}', {}, '{}', '{}')".format(task_id, do, 0, strdt, strdt)
        self.connect.cursor().execute(query).fetchall()
        self.connect.commit()
        self.connect.close()

    def delete(self, task_id):
        query = "DELETE FROM tasks WHERE id = {}".format(task_id)
        self.connect.cursor().execute(query).fetchall()
        self.connect.commit()
        self.connect.close()

    def update(self, task_id, do, status):
        dt= datetime.datetime.now()
        strdt = dt.strftime('%Y-%m-%d %H:%M:%S')
        if do is None :
            query = "UPDATE tasks SET status = {}, updated_at = '{}' WHERE id = {} ".format(status, strdt, task_id)
        elif status is None :
            query = "UPDATE tasks SET do = {}, updated_at = '{}' WHERE id = {} ".format(do, strdt, task_id)
        else :
            query = "UPDATE tasks SET do = {}, status = {}, updated_at = '{}' WHERE id = {} ".format(do, status, strdt, task_id)
        self.connect.cursor().execute(query).fetchall()
        self.connect.commit()
        self.connect.close()


@app.route("/")
def show():
    db = Database()
    if db.task_number != 0:
        return db.show()
    else :
        result = {"tasks": []}
        return jsonify(result)


@app.route("/new")
def new():
    do = request.args.get("do")
    if do is None:
        return redirect(url_for('show'))
    else :
        db = Database()
        db.new(do)
        return redirect(url_for('show'))


@app.route("/update")
def update():
    task_id = request.args.get("id")
    do = request.args.get("do")
    status = request.args.get("status")
    if task_id is None:
        return redirect(url_for('show'))
    else :
        db = Database()
        db.update(task_id, do, status)
        return redirect(url_for('show'))


@app.route("/delete")
def delete():
    task_id = request.args.get("id")
    if task_id is None:
        return redirect(url_for('show'))
    else :
        db = Database()
        db.delete(task_id)
        return redirect(url_for('show'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)