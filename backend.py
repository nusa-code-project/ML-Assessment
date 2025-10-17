import numpy as np
import pandas as pd
import joblib

class NusaCode:
    def __init__(self, model_path='model_nusaCode.pkl'):
        # Load model
        self.model = joblib.load(model_path)

        # Mapping skor jawaban
        self.score_mapping = {
            'a': 1.25,
            'b': 1.5,
            'c': 1.75,
            'd': 1.0
        }

        # Pilihan learning path
        self.learning_paths = [
            'Web Development',
            'Mobile Development',
            'Data & AI',
            'Product & UX'
        ]

    def predict(self, jawaban: dict):
        """
        Method inti yang mengembalikan rekomendasi.
        jawaban: dict {'Q1': 'a', 'Q2': 'b', ..., 'Q15': 'c'}
        return: list 3 learning path terbaik dengan probabilitas
        """
        input_vector = []
        missing = []

        # Validasi jawaban dan konversi ke skor
        for i in range(1, 16):
            ans = jawaban.get(f'Q{i}')
            if not ans:
                missing.append(i)
            else:
                input_vector.append(self.score_mapping.get(ans, 0))

        if missing:
            raise ValueError(f"Jawaban soal nomor {', '.join(map(str, missing))} belum diisi!")

        input_vector = np.array(input_vector).reshape(1, -1)

        # DataFrame jika model membutuhkan nama kolom
        if hasattr(self.model, "feature_names_in_"):
            df_input = pd.DataFrame(input_vector, columns=self.model.feature_names_in_)
        else:
            df_input = pd.DataFrame(input_vector)

        # Prediksi probabilitas
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

        return tiga_terbaik
