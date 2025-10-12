from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load model
model = joblib.load('data_nusaCode.pkl')


score_mapping = {'a': 1.25, 'b': 1.5, 'c': 1.75, 'd': 1.0}


learning_paths = ['Web Development', 'Mobile Development', 'Data & AI', 'Product & UX']


@app.route('/')
def home():
    return render_template('question.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form


    input_vector = []
    for key in sorted(data.keys()):
        ans = data[key]
        input_vector.append(score_mapping.get(ans, 0))

    input_vector = np.array(input_vector).reshape(1, -1)


    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_vector)[0]
    else:

        pred = model.predict(input_vector)[0]
        probs = np.zeros(len(learning_paths))
        probs[int(pred)] = 1.0


    top_indices = probs.argsort()[::-1][:3]
    tiga_terbaik = []
    for idx in top_indices:
        tiga_terbaik.append((learning_paths[idx], f"{probs[idx]*100:.2f}"))

    return render_template('result.html', tiga_terbaik=tiga_terbaik)


if __name__ == '__main__':
    app.run(debug=True)
