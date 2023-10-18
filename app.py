#import library
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#create a database or connect to an existing one
conn = sqlite3.connect('tasks.db')

#create a cursor object to execute SQL queries
cursor = conn.cursor()

#create a table for tasks if it doesn't exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               task TEXT NOT NULL,
               completed INTEGER DEFAULT 0
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

#add task to the database
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

#delete app from the database
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

#Mark task as completed or not completed
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)