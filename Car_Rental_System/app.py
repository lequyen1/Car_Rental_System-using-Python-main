from django import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime

import os
from werkzeug.utils import secure_filename

from django import db
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "car_rental_secret_123"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================== DATABASE ==================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Quyenle123",
        database="car_rental_system"
    )
# ================== LOAD CARS ==================
def load_cars():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE status IN ('Available', 'approved')")
    cars = cursor.fetchall()

    conn.close()
    return cars

# ================== ROUTES ==================
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cars')
def view_cars():
    cars = load_cars()
    return render_template('cars.html', cars=cars)

# ================== RENT CAR ==================
@app.route('/rent', methods=['GET'])
def rent_car():

    if 'user' not in session:
        flash("Please log in to rent a car.")
        return redirect(url_for('login'))

    car_id = request.args.get("car_id")  # lấy car_id từ URL

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE status IN ('Available', 'approved')")
    cars = cursor.fetchall()

    selected_car = None

    if car_id:
        cursor.execute("SELECT * FROM cars WHERE id=%s", (car_id,))
        selected_car = cursor.fetchone()

    conn.close()

    return render_template(
        'rent.html',
        cars=cars,
        selected_car=selected_car
    )

@app.route('/rental_history') # Xem lịch sử thuê xe
def rental_history():

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT rentals.*, cars.name, cars.image
        FROM rentals
        JOIN cars ON rentals.car_id = cars.id
        WHERE rentals.user_id = %s
        ORDER BY rentals.id DESC
    """, (user_id,))

    history = cursor.fetchall()
    conn.close()

    return render_template('rental_history.html', history=history)

@app.route('/rent_again/<int:car_id>') # Thuê lại xe đã thuê trước đó
def rent_again(car_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor()

    # Kiểm tra xe có tồn tại không
    cursor.execute("SELECT price, status FROM cars WHERE id=%s", (car_id,))
    car = cursor.fetchone()

    if not car:
        conn.close()
        return "Car not found"

    price, car_status = car

    if car_status != 'Available':
        conn.close()
        return "This car is not available."

    # Demo: thuê 1 ngày từ hôm nay
    cursor.execute("""
        INSERT INTO rentals (user_id, car_id, start_date, end_date, total_price, status)
        VALUES (%s, %s, CURDATE(), CURDATE(), %s, 'Rented')
    """, (user_id, car_id, price))

    cursor.execute("""
        UPDATE cars
        SET status='Rented'
        WHERE id=%s
    """, (car_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('rental_history'))

# ================== payment ==================
@app.route("/payment", methods=["GET", "POST"])
def payment():

    car_id = request.form.get("car_id")
    start = request.form.get("rental_date")
    end = request.form.get("return_date")

    # Check dữ liệu
    if not car_id or not start or not end:
        return "Missing data!"

    # Lấy giá từ DB
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars WHERE id=%s", (car_id,))
    car = cursor.fetchone()

    cursor.close()
    conn.close()

    if not car:
        return "Car not found!"

    price = car["price"]
    discount = car["discount"]

    # Tính ngày
    d1 = datetime.strptime(start, "%Y-%m-%d")
    d2 = datetime.strptime(end, "%Y-%m-%d")

    days = (d2 - d1).days
    if days <= 0:
        days = 1

    # Tính tiền
    total = price * days

    if discount > 0:
        total -= total * discount / 100

    return render_template(
        "payment.html",
        car=car,
        car_id=car_id,
        start=start,
        end=end,
        days=days,
        total=int(total)
    )

@app.route("/pay_success", methods=["POST"])
def pay_success():

    if 'user' not in session:
        return redirect(url_for('login'))

    car_id = request.form.get("car_id")
    start = request.form.get("rental_date")
    end = request.form.get("return_date")
    total = request.form.get("total")

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor()

    # Lưu rental với trạng thái Rented
    cursor.execute("""
        INSERT INTO rentals (user_id, car_id, start_date, end_date, total_price, status)
        VALUES (%s, %s, %s, %s, %s, 'Rented')
    """, (user_id, car_id, start, end, total))

    # Cập nhật xe thành Rented
    cursor.execute("""
        UPDATE cars
        SET status='Rented'
        WHERE id=%s
    """, (car_id,))

    conn.commit()
    conn.close()

    return render_template("success.html")

# ================== RETURN CAR ==================
@app.route('/return', methods=['GET', 'POST'])
def return_car():

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        car_id = request.form['car_id']

        # Update rental thành completed
        cursor.execute("""
            UPDATE rentals
            SET status='completed'
            WHERE car_id=%s AND user_id=%s AND status='Rented'
        """, (car_id, user_id))

        # Update car về Available
        cursor.execute("""
            UPDATE cars
            SET status='Available'
            WHERE id=%s
        """, (car_id,))

        conn.commit()
        conn.close()

        return redirect(url_for('return_car'))

    # GET → lấy xe đang thuê
    cursor.execute("""
        SELECT cars.*
        FROM cars
        JOIN rentals ON cars.id = rentals.car_id
        WHERE rentals.user_id=%s
        AND rentals.status='Rented'
    """, (user_id,))

    rented_cars = cursor.fetchall()
    conn.close()

    return render_template('return.html', cars=rented_cars)

# ================== LOGIN ==================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM users
            WHERE username=%s AND password=%s
        """, (username, password))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user'] = user

            # Nếu là admin → admin panel
            if user['role'] == 'admin':
                return redirect(url_for('admin_panel'))

            # Nếu là user → home
            return redirect(url_for('home'))

        else:
            flash("Wrong username or password!")

    return render_template('login.html')

# ================== REGISTER ==================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check trùng username
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        exist = cursor.fetchone()

        if exist:
            flash("Username already exists!")
            conn.close()
            return redirect(url_for('register'))

        # Thêm user mới
        cursor.execute("""
            INSERT INTO users(username, password, role)
            VALUES(%s, %s, 'user')
        """, (username, password))

        conn.commit()
        conn.close()

        flash("Register successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')

# ================== ADMIN ==================
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():

    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))


    if request.method == 'POST':
        action = request.form['action']

        conn = get_connection()
        cursor = conn.cursor()

        if action == 'add':
            car_id = request.form['car_id']
            name = request.form['name']
            status = request.form['status']
            file = request.files['image']
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None
            rating = request.form['rating']
            discount = request.form['discount']
            price = request.form['price']
            description = request.form['description']

            cursor.execute("""
                INSERT INTO cars (id, name, status, image, rating, discount, price, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (car_id, name, status, filename, rating, discount, price, description))

        elif action == 'edit':
            car_id = request.form['car_id']
            name = request.form['name']
            status = request.form['status']
            file = request.files.get('image')
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None
            rating = request.form['rating']
            discount = request.form['discount']
            price = request.form['price']
            description = request.form['description']

            cursor.execute("""
                UPDATE cars
                SET name=%s, status=%s, image=%s, rating=%s, discount=%s, price=%s, description=%s
                WHERE id=%s
            """, (name, status, filename, rating, discount, price, description, car_id))

        elif action == 'remove':
            car_id = request.form['car_id']

            cursor.execute(
                "DELETE FROM cars WHERE id=%s",
                (car_id,)
            )

        conn.commit()
        conn.close()

        return redirect(url_for('admin_panel'))

    # Load tất cả xe
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cars")
    all_cars = cursor.fetchall()

    # Load xe chờ duyệt
    cursor.execute("SELECT * FROM cars WHERE status='pending'")
    pending_cars = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        all_cars=all_cars,
        pending_cars=pending_cars
    )

# ================== LOGOUT ==================
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ================== FORGOT PASSWORD ==================
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        #cursor = mysql.connection.cursor()
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET password=%s WHERE username=%s",
                (new_password, username)
            )
            conn.commit()

            flash("Password reset successful. Please login.")
            return redirect(url_for('login'))
        else:
            flash("Username not found.")

    return render_template('forgotPass.html')

# ================== PROFILE ==================
@app.route('/profile')
def profile():

    # Chưa login → về login
    if 'user' not in session:
        flash("Please login first!")
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    conn.close()

    return render_template('profile.html', user=user)

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():

    if 'user' not in session:
        return redirect('/login')

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute("""
            UPDATE users
            SET full_name=%s, email=%s, phone=%s
            WHERE id=%s
        """, (full_name, email, phone, user_id))

        conn.commit()
        conn.close()

        return redirect('/profile')

    conn.close()
    return render_template('edit_profile.html', user=user)

# ================== FAVORITE ==================
@app.route('/add_favorite/<int:car_id>')    #Thêm xe vào danh sách yêu thích
def add_favorite(car_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor()

    # Check đã tồn tại chưa
    cursor.execute("""
        SELECT * FROM favorites
        WHERE user_id=%s AND car_id=%s
    """, (user_id, car_id))

    exist = cursor.fetchone()

    if not exist:
        cursor.execute("""
            INSERT INTO favorites (user_id, car_id)
            VALUES (%s, %s)
        """, (user_id, car_id))

        conn.commit()

    conn.close()

    return redirect(request.referrer)

@app.route('/favorites')    #Xem danh sách yêu thích
def view_favorites():

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT cars.*
        FROM cars
        JOIN favorites ON cars.id = favorites.car_id
        WHERE favorites.user_id = %s
    """, (user_id,))

    favorite_cars = cursor.fetchall()

    conn.close()

    return render_template('favorites.html', cars=favorite_cars)

@app.route('/remove_favorite/<int:car_id>') #Xóa khỏi danh sách yêu thích
def remove_favorite(car_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favorites
        WHERE user_id=%s AND car_id=%s
    """, (user_id, car_id))

    conn.commit()
    conn.close()

    return redirect(url_for('view_favorites'))

# ================== MY CARS ==================
@app.route('/my_cars')
def my_cars():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('verify_docs'))

# ================== My Rental Cars ==================
@app.route('/my_rental_cars')
def my_rental_cars():

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM cars
        WHERE owner_id = %s
        ORDER BY id DESC
    """, (user_id,))

    my_cars = cursor.fetchall()

    conn.close()

    return render_template('my_cars.html', cars=my_cars)

@app.route('/edit_my_car/<int:car_id>', methods=['GET', 'POST'])    #Chỉnh sửa xe của mình
def edit_my_car(car_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Kiểm tra xe có phải của user không
    cursor.execute("""
        SELECT * FROM cars
        WHERE id=%s AND owner_id=%s
    """, (car_id, user_id))

    car = cursor.fetchone()

    if not car:
        conn.close()
        return "Unauthorized access!"

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE cars
            SET name=%s, price=%s, description=%s
            WHERE id=%s AND owner_id=%s
        """, (name, price, description, car_id, user_id))

        conn.commit()
        conn.close()

        return redirect(url_for('my_rental_cars'))

    conn.close()
    return render_template('edit_my_car.html', car=car)

@app.route('/delete_my_car/<int:car_id>')   #Xóa xe của mình 
def delete_my_car(car_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cars
        WHERE id=%s AND owner_id=%s
    """, (car_id, user_id))

    user_id = session['user']['id']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cars
        WHERE id=%s AND owner_id=%s
    """, (car_id, user_id))

    conn.commit()
    conn.close()

    return redirect(url_for('my_rental_cars'))

# ================== VERIFY DOCUMENTS ==================
@app.route('/verify_docs', methods=['GET','POST'])
def verify_docs():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        cccd = request.files['cccd']
        license = request.files['license']
        cavet = request.files['cavet']

        cccd_name = secure_filename(cccd.filename)
        license_name = secure_filename(license.filename)
        cavet_name = secure_filename(cavet.filename)

        cccd.save(os.path.join(app.config['UPLOAD_FOLDER'], cccd_name))
        license.save(os.path.join(app.config['UPLOAD_FOLDER'], license_name))
        cavet.save(os.path.join(app.config['UPLOAD_FOLDER'], cavet_name))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO user_documents
        (user_id, cccd_img, license_img, cavet_img)
        VALUES (%s,%s,%s,%s)
        """, (
            session['user']['id'],
            cccd_name,
            license_name,
            cavet_name
        ))

        conn.commit()
        conn.close()

        return redirect(url_for('add_car'))

    return render_template('verify_documents.html')

# ================== ADD CAR ==================
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():

    # Chỉ user mới được đăng xe
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        name = request.form['name']
        file = request.files['image']

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        price = request.form['price']
        description = request.form['description']

        owner_id = session['user']['id']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cars (name, status, image, price, description, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            name,
            'pending',
            filename,
            price,
            description,
            owner_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for('my_cars'))

    return render_template('add_car.html')

# ================== Approve CAR ==================
@app.route('/approve_car/<int:car_id>')
def approve_car(car_id):

    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cars
        SET status='approved'
        WHERE id=%s
    """, (car_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_panel'))

# ================== REJECT CAR ==================
@app.route('/reject_car/<int:car_id>')
def reject_car(car_id):

    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cars
        WHERE id=%s AND status='pending'
    """, (car_id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_panel'))


# ================== RUN ==================
if __name__ == '__main__':
    app.run(debug=True)
