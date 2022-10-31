from flask import Flask, render_template, request, url_for, redirect, session, Response
import cv2
import numpy as np
import sys
import time
from flask_ngrok import run_with_ngrok
import smtplib
import ssl
from email.message import EmailMessage
from flask import Flask, render_template, request, url_for, redirect, session, flash, send_from_directory
from flask_mysqldb import MySQL
from datetime import timedelta
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os


app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=5)


app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config['MYSQL_PASSWORD'] = "Aadrij2005"
app.config['MYSQL_DB'] = "smartbell_info"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)
# ran_int = '5342'


# run_with_ngrok(app)

movement_count = 0

cap = cv2.VideoCapture(0)


def email_alert(to):
    email_sender = 'croptimizecorp@gmail.com'
    email_password = "gtgxkleezkwxzssd"
    email_receiver = to

    subject = "Movement Detected"
    body = """
    There might be someone or something at your door, check your stream 
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def gen_frames():
    while True:
        success, frame1 = cap.read()
        success, frame2 = cap.read()

        if not success:
            break
        else:
            global movement_count
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(
                dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 20000:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Movement'),
                            (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                movement_count = movement_count + 1
                print(movement_count)
                if movement_count == 50:
                    movement_count = 0
                    email_alert("abdulhannanm85@gmail.com")
                    continue
                else:
                    break
            ret, buffer = cv2.imencode(".jpg", frame1)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "GET":
        if "loggedin" in session:
            return redirect(url_for('home'))
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userlist WHERE gmail=%s AND password=%s", (email, password,))
        record = cursor.fetchone()
        try:
            rec_list = list(record.keys())
            val_list = list(record.values())
            ind = rec_list.index("first")
            user = val_list[ind]
            print(user)
        except:
            print("retry")
        if record:
            print(record)
            session["loggedin"] = True
            session["username"] = user
            return redirect(url_for("inhome"))
        else:
            print("Retry")
    return render_template("login.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
