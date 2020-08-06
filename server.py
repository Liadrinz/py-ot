import json

from flask import Flask, request
from utils import ot

app = Flask(__name__)

@app.route('/ot')
def get_ot():
    old = request.form.get('oldDelta')
    new = request.form.get('delta')
    old = json.loads(old)
    new = json.loads(new)
    return json.dumps(ot(old, new), ensure_ascii=False)