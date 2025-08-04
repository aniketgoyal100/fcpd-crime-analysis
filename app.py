from flask import Flask, render_template, request
import pandas as pd
import json
import os 

app = Flask(__name__)
columns = [
    "REPORT_ID", "CASE_NUMBER", "OFFENSE", "DATE_REPORTED", "TIME", 
    "BLOCK", "CITY", "STATE", "ZIP"
]

df = pd.read_csv("CrimeReports.csv", header=None, names=columns)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    zipcode = request.form["zipcode"]
    try:
        zipcode = int(zipcode)
    except ValueError:
        return "Invalid ZIP code"
    print(df.columns)
    # Filter by ZIP
    filtered = df[df["ZIP"] == zipcode]
    if filtered.empty:
        return f"No crime data found for ZIP code {zipcode}."

    # Group by OFFENSE type
    offense_counts = filtered["OFFENSE"].value_counts()
    labels = list(offense_counts.index)
    values = list(offense_counts.values)
    total = sum(values)
    most_common = labels[0] if labels else "N/A"

    return render_template(
        "results.html",
        zipcode=zipcode,
        json_labels=json.dumps(labels),
        json_values=json.dumps([int(v) for v in values]),
        labels=labels,
        values=[int(v) for v in values],
        total_crimes=sum(values),
        most_common=most_common,
        zip=zip
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host = "0.0.0.0", port=port)
