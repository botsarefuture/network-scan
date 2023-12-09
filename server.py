from flask import Flask, jsonify, request
from pymongo import MongoClient
import time

app = Flask(__name__)
mongo_client = MongoClient("mongodb://10.0.0.1:27017/?directConnection=true&authMechanism=DEFAULT")
db = mongo_client["scan"]
ips = db["ips"]
results = db["results"]
ip_visits_collection = db["ip_visits"]  # New collection for storing IP visits


def get_ips():
    ip = ips.find_one_and_update({"gaved": False}, {"$set": {"gaved": True}}, projection={"ip": True})
    return ip["ip"] if ip else None


@app.route("/get_ip", methods=["GET"])
def get_ip():
    ip = get_ips()

    # Track IP visits
    timestamp = int(time.time())
    if ip:
        client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        ip_visits_collection.insert_one({"client_ip": client_ip, "ip": ip, "timestamp": timestamp})

    return jsonify({"ip": ip}) if ip else jsonify({"error": "No more ips"})


@app.route("/submit_results", methods=["POST"])
@app.route("/submit_results/", methods=["POST"])
def submit_results():
    data = request.json
    results.insert_one(data)
    return jsonify({"message": "Results received successfully"})


@app.route("/add_ip", methods=["POST"])
def add_ip():
    ip_to_add = request.json.get("ip")
    ips.insert_one({"ip": ip_to_add, "gaved": False})
    return jsonify({"message": "IP added successfully"})


@app.route("/get_results", methods=["GET"])
def get_results():
    results_data = str(list(results.find()))
    return jsonify(results_data)


@app.route("/get_ip_visits_in_hour", methods=["GET"])
def get_ip_visits_in_hour():
    current_time = int(time.time())
    hour_ago = current_time - 3600
    
    # Filter and retrieve IP visits within the last hour from the database
    recent_ip_visits = str(list(ip_visits_collection.find({"timestamp": {"$gt": hour_ago}})))
    
    return jsonify(recent_ip_visits)


if __name__ == "__main__":
    app.run(debug=True)
