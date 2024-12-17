from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to convert 24-hour time to 12-hour format
def to_12_hour_format(hour, minute):
    suffix = "AM" if hour < 12 else "PM"
    hour = hour if hour <= 12 else hour - 12
    hour = 12 if hour == 0 else hour
    return f"{hour}:{minute:02d} {suffix}"

# Initialize slots for current and tomorrow's date
dates = [
    datetime.now().strftime('%Y-%m-%d'),
    (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
]
time_slots = {
    date: [{"time": to_12_hour_format(h, m), "associates": []} for h in range(24) for m in (0, 30)]
    for date in dates
}

@app.route("/")
def home():
    return render_template("index.html", dates=dates)

@app.route("/get_slots", methods=["GET"])
def get_slots():
    date = request.args.get("date")
    if date not in time_slots:
        return jsonify({"error": "Invalid date"}), 400
    return jsonify(time_slots[date])

@app.route("/submit", methods=["POST"])
def submit():
    alias = request.form.get("alias")
    selected_time = request.form.get("time")
    selected_date = request.form.get("date")

    if selected_date not in time_slots:
        return jsonify({"message": "Invalid date"}), 400

    for slot in time_slots[selected_date]:
        if slot["time"] == selected_time:
            if len(slot["associates"]) < 2:
                slot["associates"].append(alias)
                return jsonify({"message": "Appointment booked!"})
            else:
                return jsonify({"message": "Time slot is full!"}), 400

    return jsonify({"message": "Invalid time slot!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
