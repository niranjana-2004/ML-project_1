from flask import Flask, request, render_template_string
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

matplotlib.use("Agg")
app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
df = pd.read_csv("student_data.csv")
avg_studytime = round(df["studytime"].mean(), 2)
avg_grade = round(df["G3"].mean(), 2)
corr_study_grade = round(df["studytime"].corr(df["G3"]), 2)


def create_plot(x, y, xlabel, ylabel, title):
    plt.figure(figsize=(4,3))
    plt.scatter(x, y, alpha=0.6)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    return base64.b64encode(buf.read()).decode("utf-8")

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
.modal {
            display: none;
            position: fixed;
            z-index: 10;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.4);
        }
        .modal-content {
            background: white;
            padding: 20px;
            width: 300px;
            margin: 150px auto;
            border-radius: 8px;
            text-align: center;
        }
        .close {
            float: right;
            cursor: pointer;
            font-size: 20px;
        }

        img {
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h2>Student Performance Prediction</h2>

    <form method="post">

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

    <h3>📊 Study & Performance Statistics</h3>

<ul>
  <li><strong>Average Study Time:</strong> {{ avg_studytime }} hours</li>
  <li><strong>Average Final Grade (G3):</strong> {{ avg_grade }}</li>
  <li><strong>Correlation (Study Time vs Grade):</strong> {{ corr_study_grade }}</li>
</ul>

{% if study_plot %}
  <h3>📈 Study Time vs Final Grade</h3>
  <img src="data:image/png;base64,{{ study_plot }}" width="400">
{% endif %}
</div>

<div id="resultModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="closeModal()">&times;</span>
    <h3>Prediction Result</h3>
    <p><strong>Final Grade (G3):</strong> {{ prediction }}</p>
    <p><strong>Status:</strong> {{ status }}</p>
    <p><strong>Performance:</strong> {{ level }}</p>
  </div>
</div>

<script>
    function closeModal() {
        document.getElementById("resultModal").style.display = "none";
    }

    {% if prediction is not none %}
        document.getElementById("resultModal").style.display = "block";
    {% endif %}
</script>
</body>
</html>
"""
@app.route("/", methods=["GET","POST"])
def home():
    study_plot=None
    prediction = None
    status = None
    level = None
    studytime_plot=None
    absences_plot=None

    if request.method == "POST":
        G1 = float(request.form["G1"])
        G2 = float(request.form["G2"])
        studytime = float(request.form["studytime"])
        absences = float(request.form["absences"])

        result = model.predict([[G1, G2, studytime, absences]])
        prediction = round(result[0], 2)

        status = "Pass" if prediction >= 10 else "Fail"

        if prediction >= 15:
            level = "Excellent"
        elif prediction >= 12:
            level = "Good"
        elif prediction >= 10:
            level = "Average"
        else:
            level = "Poor"

        study_plot = create_plot(
            df["studytime"], df["G3"],
            "Study Time", "Final Grade",
            "Study Time vs Final Grade"
        )

        absences_plot = create_plot(
            df["absences"], df["G3"],
            "Absences", "Final Grade (G3)",
            "Absences vs Final Grade"
        )
    return render_template_string(
    html,
    prediction=prediction,
    status=status,
    level=level,
    study_plot=study_plot,
    avg_studytime=avg_studytime,
    avg_grade=avg_grade,
    corr_study_grade=corr_study_grade
    )
if __name__ == "__main__":
    app.run(debug=True)