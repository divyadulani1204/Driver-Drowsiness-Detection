from flask import Flask, render_template, Response
import cv2
from TEMPLATE.ML import detect_faces
app = Flask(__name__)
app.secret_key = '8f392d4becbece3d8ca57838c4de1b29eef3fb213779dc2c'

# Open webcam
cap = cv2.VideoCapture(0)

# Function to generate video frames with face detection
def generate_frames():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

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
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('video_feed'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Your login route implementation
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add your authentication logic here, for example:
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('video_feed'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

    

@app.route('/logout')
def logout():
    # Your logout route implementation
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/video_feed')
def video_feed():
    if 'username' not in session:
        return redirect(url_for('login'))
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
