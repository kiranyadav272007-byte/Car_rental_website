from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            address TEXT,
            car_name TEXT,
            rent_date TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_rental():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        car_name = request.form['car_name']
        rent_date = request.form['rent_date']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("""
            INSERT INTO rentals
            (name, phone, address, car_name, rent_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, address, car_name, rent_date))

        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add_rental.html')


@app.route('/view')
def view_rentals():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM rentals")
    rentals = c.fetchall()

    conn.close()

    return render_template('view_rentals.html', rentals=rentals)


@app.route('/delete/<int:id>')
def delete_rental(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("DELETE FROM rentals WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/view')


if __name__ == '__main__':
    app.run(debug=True)