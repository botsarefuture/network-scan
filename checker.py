import pymongo

def fetch_results_from_mongodb():
    # Connect to MongoDB (adjust connection details accordingly)
    client = pymongo.MongoClient("mongodb://10.0.0.1:27017/?directConnection=true&authMechanism=DEFAULT")
    db = client.scan
    collection = db.results

    # Fetch data from MongoDB
    data = list(collection.find({}))

    return data

def check_results(data, checked_ips):
    for result in data:
        res = result.get("results", None)
        if res is not None:
            ip = res["ip"]
            if ip not in checked_ips:
                checked_ips.add(ip)
                open_ports = res.get("open_ports", None)
                # Check if the IP has open ports
                if open_ports:
                    print(f"IP {ip} has open ports: {open_ports}")
        else:
            continue

    return checked_ips

checked_ips_set = set()

while True:
    # Fetch data from MongoDB
    data_from_mongodb = fetch_results_from_mongodb()

    # Check results for open ports only
    checked_ips_set = check_results(data_from_mongodb, checked_ips_set)

    import time
    
    time.sleep(2)
