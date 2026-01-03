from flask import Flask, request, render_template_string
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

html="""
<!DOCTYPE html>
<html>
<head>
    <title>Student Performance Predictor</title>
    <style>
        body {
    font-family: Arial, sans-serif;
    background: #f4f6f8;
}

.container {
    width: 400px;
    margin: 80px auto;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

h2 {
    text-align: center;
    color: #333;
}

label {
    display: block;
    margin-top: 15px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border-radius: 4px;
    border: 1px solid #ccc;
}

button {
    width: 100%;
    margin-top: 20px;
    padding: 10px;
    background: #007BFF;
    color: white;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background: #0056b3;
}

.result {
    margin-top: 20px;
    padding: 12px;
    background: #e8f0fe;
    text-align: center;
    font-weight: bold;
    border-radius: 5px;
}

    </style>
</head>
<body>
    <h2>Student Performance Prediction</h2>

    <form action="/predict" method="post">

        <label>G1 (First Period Grade):</label><br>
        <input type="number" name="G1" required><br><br>

        <label>G2 (Second Period Grade):</label><br>
        <input type="number" name="G2" required><br><br>

        <label>Study Time:</label><br>
        <input type="number" step="0.1" name="studytime" required><br><br>

        <label>Absences:</label><br>
        <input type="number" name="absences" required><br><br>

        <button type="submit">Predict Final Grade</button>
    </form>

    <h3>{{ prediction_text }}</h3>
</body>
</html>
"""
@app.route("/")
def home():
    prediction = None
    if request.method == "POST":
        G1 = float(request.form["G1"])
        G2 = float(request.form["G2"])
        studytime = float(request.form["studytime"])
        absences = float(request.form["absences"])

        result = model.predict([[G1, G2, studytime, absences]])
        prediction = round(result[0], 2)

    return render_template_string(html, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)