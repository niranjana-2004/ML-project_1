from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    G1 = float(request.form["G1"])
    G2 = float(request.form["G2"])
    studytime = float(request.form["studytime"])
    absences = float(request.form["absences"])

    prediction = model.predict([[G1, G2, studytime, absences]])
    result = round(prediction[0], 2)

    return render_template(
        "index.html",
        prediction_text=f"Predicted Final Grade (G3): {result}"
    )

if __name__ == "__main__":
    app.run(debug=True)
