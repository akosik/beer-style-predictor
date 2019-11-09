# Beer Style Prediction
This repo contains a main report notebook found in `notebooks/report.ipynb`
and a flask app for a POC deployment approach.

To run `notebooks/report.ipynb`:
```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
jupyter notebook
```
and select the notebook from the jupyter web-browser interface.

To run tests for flask app:
```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.:$PYTHONPATH
python3 -m unittest
```