from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib


class NusaCode:
    def __init__(self, model_path='model_nusaCode.pkl'):
        self.app = Flask(__name__)
        self.model = joblib.load(model_path)

        self.score_mapping = {
            'a': 1.25,
            'b': 1.5,
            'c': 1.75,
            'd': 1.0
        }

        self.learning_paths = [
            'Web Development',
            'Mobile Development',
            'Data & AI',
            'Product & UX'
        ]

        # Register routes
        self.register_routes()

    def register_routes(self):
        """Daftarkan semua route Flask"""
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/submit', 'submit', self.submit, methods=['POST'])

    def home(self):
        """Menampilkan halaman utama kuis"""
        return render_template('question.html')

    def submit(self):
        """Memproses form kuis dan memberikan rekomendasi"""
        data = request.form
        input_vector = []
        missing = []


        for i in range(1, 16):
            ans = data.get(f'Q{i}')
            if not ans:
                missing.append(i)
            else:
                input_vector.append(self.score_mapping.get(ans, 0))

        if missing:
            missing_str = ', '.join(str(num) for num in missing)
            return {
                'status': 'error',
                'missing': missing,
                'message': f'Jawaban soal nomor {missing_str} belum diisi!'
            }


        input_vector = np.array(input_vector).reshape(1, -1)
        if hasattr(self.model, "feature_names_in_"):
            df_input = pd.DataFrame(input_vector, columns=self.model.feature_names_in_)
        else:
            df_input = pd.DataFrame(input_vector)


        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(df_input)[0]
        else:
            pred = self.model.predict(df_input)[0]
            probs = np.zeros(len(self.learning_paths))
            probs[int(pred)] = 1.0

        # Ambil 3 path teratas
        top_indices = probs.argsort()[::-1][:3]
        tiga_terbaik = [
            {'path': self.learning_paths[idx], 'prob': f"{probs[idx]*100:.2f}%"}
            for idx in top_indices
        ]

        return render_template('result.html', tiga_terbaik=tiga_terbaik)

    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == '__main__':
    app_instance = NusaCode()
    app_instance.run()
