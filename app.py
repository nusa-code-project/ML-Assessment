from flask import Flask, render_template,request,jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load('data_nusaCode.pkl')

score_mapping = {
    'a' : 1.25,
    'b' : 1.5,
    'c' : 1.75,
    'd' : 1.00
 }

@app.route('/')
def home() :
    return render_template('./template/question.html')

@app.route('/submit', methods=['POST'])
def submit():

    try :
        jawaban = []
        for i in range(1,16):
            nilai = request.form.get(f'Nomor {i}')
            if nilai not in score_mapping :
                return jsonify({"error": f"Anda belum mengisi pilihan Nomor {i}"})
            jawaban.append(score_mapping[nilai])

        X = np.array(jawaban).reshape(1,-1)

        prediction =