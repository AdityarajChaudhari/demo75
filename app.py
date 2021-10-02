import pymysql
import numpy as np
import psycopg2
import pickle
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import warnings
from flask_sqlalchemy import SQLAlchemy
warnings.filterwarnings("ignore")

# db = pymysql.connect(host="localhost",user="root",passwd="mysql",database="adityaraj")
# cur = db.cursor()
# cur.execute("CREATE TABLE if not exists salary2 ( Experience int NOT NULL,  TestScore int NOT NULL , InterviewScore int)")
# db.commit()

app = Flask(__name__)

db = psycopg2.connect(host="ec2-52-207-47-210.compute-1.amazonaws.com",user="myomncodksvndi",password="1045ca319c733cdf9f516474fdaf51c01c7ad8437f2a09e227376e8a5045d236",database="dfhjr53cl9t2fk")
cur = db.cursor()


model = pickle.load(open('model.pkl','rb'))

@cross_origin()
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@cross_origin()
@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        experience = request.form['experience']
        test_score = request.form['test_score']
        interview_score = request.form['interview_score']
        print(experience)
        cur.execute("create table if not exists salary(experience int primary key, test_score int, interview_score int);")
        cur.execute(f"insert into salary values{(experience,test_score,interview_score)}")
        db.commit()

        feat = [[experience,test_score,interview_score]]
        pred = model.predict(feat)
        output = round(pred[0], 2)
        return render_template('index.html', prediction_text="Employee salary should be $ {}".format(output))


if __name__ == "__main__":
    app.run()