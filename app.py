from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io, base64, random

app = Flask(__name__)

def generate_patient_data(patient_number):
    return {
        "Patient Number": patient_number,
        "Blood Pressure": random.randint(80, 160),
        "Heart Rate": random.randint(50, 120),
        "Oxygen Levels": random.randint(90, 100),
        "Blood Sugar": random.randint(60, 200),
        "Cholesterol": random.randint(140, 250),
        "Doctor’s Suggestion": "Maintain a balanced diet, exercise regularly, and avoid stress."
    }

def generate_graph(data):
    labels = ["Blood Pressure", "Heart Rate", "Oxygen Levels", "Blood Sugar", "Cholesterol"]
    values = [data[key] for key in labels]
    normal_ranges = {
        "Blood Pressure": (90, 130), "Heart Rate": (60, 100),
        "Oxygen Levels": (95, 100), "Blood Sugar": (70, 140),
        "Cholesterol": (150, 200)
    }

    colors = [
        "green" if normal_ranges[label][0] <= value <= normal_ranges[label][1] else "red"
        for label, value in zip(labels, values)
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=colors)
    plt.ylim(50, 260)
    plt.ylabel("Values")
    plt.title(f"Patient {data['Patient Number']} Vitals")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{graph_url}"

def analyze_health(data):
    status = "Healthy"
    alerts = []
    diagnosis_list = []

    if not 90 <= data["Blood Pressure"] <= 130:
        alerts.append("⚠️ Blood Pressure abnormal!")
        diagnosis_list.append("Hypertension or Hypotension")

    if not 60 <= data["Heart Rate"] <= 100:
        alerts.append("⚠️ Heart Rate irregular!")
        diagnosis_list.append("Cardiac issues")

    if not 95 <= data["Oxygen Levels"] <= 100:
        alerts.append("⚠️ Low Oxygen Levels!")
        diagnosis_list.append("Respiratory condition")

    if not 70 <= data["Blood Sugar"] <= 140:
        alerts.append("⚠️ Blood Sugar out of range!")
        diagnosis_list.append("Diabetes risk")

    if not 150 <= data["Cholesterol"] <= 200:
        alerts.append("⚠️ High Cholesterol!")
        diagnosis_list.append("Heart disease risk")

    if alerts:
        status = "⚠️ Needs Attention"

    diagnosis = " and ".join(set(diagnosis_list)) if diagnosis_list else "No major issues detected."
    return status, alerts, diagnosis

@app.route("/", methods=["GET", "POST"])
def index():
    patient_data = None
    graph_url = None
    alerts = []
    diagnosis = ""

    if request.method == "POST":
        patient_number = request.form.get("patient_number", "").strip()
        if not patient_number.isdigit():
            alerts.append("❌ Invalid patient number!")
        else:
            patient_data = generate_patient_data(patient_number)
            graph_url = generate_graph(patient_data)
            patient_data["Health Status"], alerts, diagnosis = analyze_health(patient_data)

    return render_template("index.html", patient_data=patient_data, graph_url=graph_url, alerts=alerts, diagnosis=diagnosis)

if __name__ == "__main__":
    app.run(debug=True)
