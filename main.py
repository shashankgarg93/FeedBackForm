#! /usr/bin/python

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Bhullar88@localhost/Feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xpodtpifukhyry:84313a0da54862383f896de3d03260616761f516185b2ff9b24fe0d8520952d4@ec2-34-235-62-201.compute-1.amazonaws.com:5432/d2ht2ts1n0eapj'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), unique=True)
    SID = db.Column(db.String(200), unique=True)
    rating = db.Column(db.String(5))
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student = request.form['student']
        SID = request.form['SID']
        rating = request.form['affirmative']
        comments = request.form['comments']
        if student == '' or SID == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.student == student).count() == 0:
            data = Feedback(student, SID, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.debug = True
    app.run()
