from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize time slots with 2 available spots per slot
time_slots = [{"time": f"{h % 12 or 12}:{m:02d} {'AM' if h < 12 else 'PM'}", "associates": []}
              for h in range(24) for m in (0, 30)]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    alias = data.get("alias")
    selected_time = data.get("time")

    for slot in time_slots:
        if slot["time"] == selected_time:
            if len(slot["associates"]) < 2:  # Allow up to 2 associates per slot
                slot["associates"].append(alias)
                return jsonify({"message": "Appointment booked successfully!", "time": selected_time})
            else:
                return jsonify({"message": "This time slot is full!"}), 400

    return jsonify({"message": "Invalid time slot!"}), 400


@app.route("/get_slots", methods=["GET"])
def get_slots():
    # Return time slots with associate details
    return jsonify(time_slots)


if __name__ == "__main__":
    app.run(debug=True)
