import requests
from datetime import datetime, timezone
import dateutil.parser

def lambda_handler(event, context):
    # Read parameters from Amazon Connect event
    parameters = event.get("Details", {}).get("Parameters", {})
    bus_stop = parameters.get("BusStopCode")
    service_no = parameters.get("ServiceNo")

    if not bus_stop or not service_no:
        return {
            "FinalArivalTime": "Missing BusStopCode or ServiceNo"
        }

    # LTA DataMall API
    url = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"
    headers = {
        "AccountKey": "hN1R2sLbRe2GnXRYEtuZ6Q==",
        "Accept": "application/json"
    }
    params = {
        "BusStopCode": bus_stop,
        "ServiceNo": service_no
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except Exception as e:
        print("Request failed:", str(e))
        return {
            "FinalArivalTime": "Unable to reach bus service"
        }

    # Debug info (visible in CloudWatch)
    print("HTTP Status:", response.status_code)
    print("Response body (first 300 chars):", response.text[:300])

    if response.status_code != 200:
        return {
            "FinalArivalTime": f"LTA API error {response.status_code}"
        }

    try:
        data = response.json()
    except Exception as e:
        print("JSON decode error:", str(e))
        return {
            "FinalArivalTime": "Invalid response from LTA API"
        }

    services = data.get("Services", [])
    if not services:
        return {
            "FinalArivalTime": "No arrival information available"
        }

    eta = services[0].get("NextBus", {}).get("EstimatedArrival")
    if not eta:
        return {
            "FinalArivalTime": "Arrival time not available"
        }

    # Parse ETA and compute time difference
    arrival_time = dateutil.parser.isoparse(eta).astimezone(timezone.utc)
    now = datetime.now(timezone.utc)

    seconds = int((arrival_time - now).total_seconds())

    if seconds <= 0:
        return {
            "FinalArivalTime": "Arriving now"
        }

    minutes = seconds // 60
    secs = seconds % 60

    return {
        "FinalArivalTime": f"Arriving in {minutes} minutes and {secs} seconds"
    }
