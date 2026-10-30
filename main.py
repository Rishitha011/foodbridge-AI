from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# In-memory mock database for the hackathon prototype
donors = [
    {"id": 1, "name": "Fresh Bakery", "lat": 17.3850, "lon": 78.4867, "item": "Bread & Pastries", "quantity_kg": 15},
    {"id": 2, "name": "City Grocers", "lat": 17.3900, "lon": 78.4900, "item": "Fresh Vegetables", "quantity_kg": 50}
]

shelters = [
    {"id": 101, "name": "Hope Community Kitchen", "lat": 17.3860, "lon": 78.4880, "demand": "Vegetables & Produce"},
    {"id": 102, "name": "Sunrise Shelter", "lat": 17.3950, "lon": 78.4950, "demand": "Bakery Items"}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    # Simple Euclidean distance approximation for prototype demo
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

@app.route('/api/match', methods=['POST'])
def match_surplus():
    matches = []
    for donor in donors:
        # Find the closest shelter based on lat/lon
        closest_shelter = min(
            shelters, 
            key=lambda s: calculate_distance(donor["lat"], donor["lon"], s["lat"], s["lon"])
        )
        
        matches.append({
            "donor_name": donor["name"],
            "item": donor["item"],
            "quantity_kg": donor["quantity_kg"],
            "matched_organization": closest_shelter["name"],
            "status": "Matched Successfully"
        })
        
    return jsonify({"status": "success", "matches": matches})

@app.route('/api/surplus', methods=['POST'])
def add_surplus():
    data = request.json
    new_donor = {
        "id": len(donors) + 1,
        "name": data.get("donorName"),
        "lat": data.get("lat", 17.3850),
        "lon": data.get("lon", 78.4867),
        "item": data.get("foodItem"),
        "quantity_kg": data.get("quantity")
    }
    donors.append(new_donor)
    return jsonify({"status": "success", "message": "Surplus added and queued for matching!", "donor": new_donor})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
