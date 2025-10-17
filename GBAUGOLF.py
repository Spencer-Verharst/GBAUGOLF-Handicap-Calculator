from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

user_scores = {}

def calculate_handicap(rounds):
    if not rounds:
        return None
    
    recent_rounds = rounds[-5:]
    round_totals = [sum(r) for r in recent_rounds]
    best_rounds = sorted(round_totals)[:2]
    average = sum(best_rounds) / len(best_rounds)
    handicap = (average - 72) * 0.96  # Assuming Course Rating = 72
    return round(handicap, 1)

@app.route('/submit_round', methods=['POST'])
def submit_round():
    round_data = request.get_json()
    name = round_data.get("name")
    golf_scores = round_data.get("scores")  # Fixed key to match frontend

    if not name or not golf_scores or len(golf_scores) != 18:
        return jsonify({"error": "You must submit an 18-hole score."}), 400

    if name not in user_scores:
        user_scores[name] = []

    user_scores[name].append(golf_scores)
    handicap = calculate_handicap(user_scores[name])

    return jsonify({
        "message": f"The round for {name} is saved.",
        "rounds_played": len(user_scores[name]),
        "handicap": handicap
    })

@app.route('/')
def index():
    return send_from_directory('.', 'GBAUGOLF.html')

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)