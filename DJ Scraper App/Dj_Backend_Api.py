
# Backend API for DJ Venue App
# Flask app to serve scraped data to mobile app frontend

from flask import Flask, jsonify
from Dj_Scraper import aggregate_data

app = Flask(__name__)

@app.route("/api/djs", methods=["GET"])
def get_djs():
    try:
        data = aggregate_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
