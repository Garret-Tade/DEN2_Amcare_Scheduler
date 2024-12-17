from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to format time as 12-hour AM/PM
def to_12_hour_format(hour, minute):
    suffix = "AM" if hour < 12 else "PM"
    hour = hour if hour <= 12 else hour - 12
    hour = 12 if hour == 0 else hour
    return f"{hour}:{minute:02d} {suffix}"

# Initialize slots for two dates with 30-minute increments across 24 hours
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

@app.route("/book_slot", methods=["POST"])
def book_slot():
    alias = request.form.get("alias")
    selected_time = request.form.get("time")
    selected_date = request.form.get("date")

    if selected_date not in time_slots:
        return jsonify({"message": "Invalid date"}), 400

    for slot in time_slots[selected_date]:
        if slot["time"] == selected_time:
            if len(slot["associates"]) < 2:
                slot["associates"].append(alias)
                return jsonify({"message": "Appointment booked successfully!"})
            else:
                return jsonify({"message": "Time slot is full!"}), 400

    return jsonify({"message": "Invalid time slot!"}), 400

@app.route("/get_booked_slots", methods=["GET"])
def get_booked_slots():
    date = request.args.get("date")
    if date not in time_slots:
        return jsonify({"error": "Invalid date"}), 400

    booked_slots = [slot for slot in time_slots[date] if slot["associates"]]
    return jsonify(booked_slots)

if __name__ == "__main__":
    app.run(debug=True)
