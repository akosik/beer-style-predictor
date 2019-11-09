"""
Defines a flask api for serving beer style predictions
"""

import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

from src.utils import check_input

app = Flask(__name__)
api = Api(app)

project_dir = Path(os.path.dirname(__file__)).parent

feats = joblib.load(project_dir / 'assets' / 'feat_list.pk')

parser = reqparse.RequestParser()
for feat in feats:
    parser.add_argument(feat)

pipeline = joblib.load(project_dir / 'assets' / 'rf_model.pk')

class StylePredictor(Resource):
    @staticmethod
    def get():
        args = parser.parse_args()

        # construct pandas DataFrame from args dictionary
        # convert all singelton columns to lists of length 1
        x = pd.DataFrame({col_header: [col] if not isinstance(col, list) else col
                          for col_header, col in args.items()})

        is_clean, message = check_input(x)
        if not is_clean:
            abort(404, message=message)

        prediction = pipeline.predict(x)

        return {'prediction': int(prediction[0])}


api.add_resource(StylePredictor, '/style/predict')

if __name__ == '__main__':
    app.run(debug=True)
