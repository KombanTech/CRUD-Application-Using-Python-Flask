from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="komban",
    database="crud_app"
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    department = request.form['department']
    college_name = request.form['college_name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    
    cursor.execute("INSERT INTO users (name, department, college_name, phone_number, email) VALUES (%s, %s, %s, %s, %s)", 
                   (name, department, college_name, phone_number, email))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        college_name = request.form['college_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        
        cursor.execute("UPDATE users SET name=%s, department=%s, college_name=%s, phone_number=%s, email=%s WHERE id=%s",
                       (name, department, college_name, phone_number, email, id))
        db.commit()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    return render_template('edit.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
