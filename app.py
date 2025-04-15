import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, render_template, request, jsonify

from chat import get_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.get("/")
def index_get():
    return render_template("base.html", charset='utf-8').encode('utf-8')

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    return jsonify({"answer": response}), 200, {'Content-Type': 'application/json; charset=utf-8'}

    # message = {"answer": response}
    # return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)


