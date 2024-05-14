import winsound
import ctypes
import cv2
from ML import detect_faces

from flask import Flask, Response, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__,static_url_path='/static')
app.secret_key = '8f392d4becbece3d8ca57838c4de1b29eef3fb213779dc2c'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Open webcam
cap = cv2.VideoCapture(0)

# Function to generate video frames with face detection
def generate_frames():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret or frame is None:
            # If frame is empty or capture fails, log the error and continue
            print("Error: Empty frame or capture failed")
            continue

        # Process frame for face and eye detection
        if detect_faces(frame):
            # Driver is sleeping, trigger alert
            winsound.Beep(1000, 2000)  # Beep for 2 seconds
            ctypes.windll.user32.MessageBoxW(0, "Driver is sleeping!", "Driver Alert", 1)

        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Yield the encoded frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# @app.route('/')
# def index():
#     if 'username' in session:
#         return redirect(url_for('video_feed'))
#     return render_template('login.html')
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['signup-username']
        email = request.form['signup-email']
        password = request.form['signup-password']

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'Email already exists. Please choose a different email.'

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('login.html')


# @app.route('/login', methods=['POST'])
# def login():
#     # Your login route implementation
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         user = User.query.filter_by(username=username).first()
#         if user and bcrypt.check_password_hash(user.password, password):
#             session['username'] = username
#             return redirect(url_for('video_feed'))
#         else:
#             return 'Invalid username or password'
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     # Your logout route implementation
#     session.pop('username', None)
#     return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('video_feed'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/video_feed')
def video_feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(port=5501, debug=True)
