from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize time slots with 2 spots per slot
time_slots = [{"time": f"{h:02d}:{m:02d}", "associates": []}
              for h in range(24) for m in (0, 30)]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_slots", methods=["GET"])
def get_slots():
    return jsonify(time_slots)

@app.route("/submit", methods=["POST"])
def submit():
    alias = request.form.get("alias")
    selected_time = request.form.get("time")

    for slot in time_slots:
        if slot["time"] == selected_time:
            if len(slot["associates"]) < 2:
                slot["associates"].append(alias)
                return jsonify({"message": "Appointment booked!"})
            else:
                return jsonify({"message": "Time slot is full!"}), 400

    return jsonify({"message": "Invalid time slot!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
