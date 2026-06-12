import joblib
import os
import pandas as pd


class ObesityModelWrapper:

    def __init__(self):
        self.model_path = os.path.join(
            os.path.dirname(__file__),
            "obesity_model.pkl"
        )

        self.pipeline = self._load_model()

    def _load_model(self):

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model tidak ditemukan: {self.model_path}"
            )

        return joblib.load(self.model_path)

    def predict(
        self,
        age: int,
        gender: str,
        height_cm: float,
        weight_kg: float
    ) -> str:

        gender = gender.capitalize()

        if gender not in ["Male", "Female"]:
            raise ValueError(
                "Gender harus Male atau Female"
            )

        input_df = pd.DataFrame([{
            "Age": age,
            "Gender": gender,
            "Height": height_cm / 100,
            "Weight": weight_kg
        }])

        prediction = self.pipeline.predict(
            input_df
        )

        return str(prediction[0])

model = ObesityModelWrapper()

def predict_obesity(
    age: int,
    gender: str,
    height_cm: float,
    weight_kg: float
):

    return model.predict(
        age,
        gender,
        height_cm,
        weight_kg
    )