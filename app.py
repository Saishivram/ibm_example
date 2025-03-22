from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, send_file
from flask_cors import CORS
import requests
import json
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ibm_environmental_intelligence_app_secret"
CORS(app, resources={r"/*": {"origins": "*"}})

# ================================
# TEMPLATES (DO NOT REMOVE)
# ================================
TEMPLATES = {
    "stationary": {
        "customID": {
            "id": "1705630062608384"
        },
        "onBehalfOfClient": {
            "companyId": "2652286536908800",
            "companyName": "Rebecca Vasquez"
        },
        "organisation": {
            "departmentId": "6477322324541440",
            "departmentName": "Henrietta Park"
        },
        "requestType": "ACTUAL",
        "location": {
            "country": "Dominican Republic",
            "stateProvince": "QC",
            "zipPostCode": "G6T 1F9",
            "city": "Bickirjo"
        },
        "site": {
            "siteId": "3247133727653888",
            "siteName": "Thomas Keller",
            "buildingId": "380135630962688",
            "buildingName": "Julia Bell"
        },
        "timePeriod": {
            "year": 2021,
            "month": 1
        },
        "activityData": {
            "sector": "Energy",
            "fuelName": "Coal tar",
            "fuelAmount": "1.5",
            "fuelUnit": "metric ton",
            "hvBasis": "Not applicable"
        }
    },
    "fugitive": {
        "customID": {
            "id": "6211504336535552"
        },
        "onBehalfOfClient": {
            "companyId": "708157594664960",
            "companyName": "Alan Wolfe"
        },
        "organisation": {
            "departmentId": "5920042151575552",
            "departmentName": "Jimmy Barnett"
        },
        "requestType": "ACTUAL",
        "location": {
            "country": "Guinea-Bissau",
            "stateProvince": "AB",
            "zipPostCode": "L0N 2R9",
            "city": "Sopemuv"
        },
        "site": {
            "siteId": "632932941168640",
            "siteName": "Hunter Parks",
            "buildingId": "4197294742175744",
            "buildingName": "Harry Ryan"
        },
        "timePeriod": {
            "year": 2021,
            "month": 1
        },
        "activityData": {
            "refrigerantName": "R-404A",
            "refrigerantInventoryBeginning": "10",
            "refrigerantInventoryEnd": "2",
            "refrigerantsPurchasedFromProducers": "6",
            "refrigerantsProvidedByManufacturers": "2",
            "refrigerantsAddedToEquipment": "3",
            "refrigerantReturnedAfterRecycling": "0",
            "refrigerantSales": "3",
            "refrigerantLeftInEquipment": "4",
            "refrigerantReturnedToSuppliers": "1",
            "refrigerantForRecycling": "0",
            "refrigerantForDestruction": "0",
            "totalChargeNewEquipment": "0",
            "totalChargeRetrofitted": "0",
            "originalChargeEquipment": "0",
            "totalChargeEquipmentRetroAway": "0",
            "unitOfMeasurement": "kilogram"
        }
    },
    "mobile": {
        "customID": {
            "id": "2533309844291584"
        },
        "onBehalfOfClient": {
            "companyId": "6828322780610560",
            "companyName": "Sam Sims"
        },
        "organisation": {
            "departmentId": "3123310890057728",
            "departmentName": "Kyle Webster"
        },
        "requestType": "ACTUAL",
        "location": {
            "country": "French Southern Territories",
            "stateProvince": "NL",
            "zipPostCode": "M3G 3H8",
            "city": "Ligenah"
        },
        "site": {
            "siteId": "470430345330688",
            "siteName": "Isaac Jimenez",
            "buildingId": "8042437509382144",
            "buildingName": "Jorge Kelly"
        },
        "timePeriod": {
            "year": 2021,
            "month": 1
        },
        "activityData": {
            "vehicleType": "Heavy Duty Vehicle – Rigid – Gasoline – Year 2005-present",
            "fuelUsed": "Gasoline",
            "fuelAmount": "20",
            "unitOfFuelAmount": "US Gallon"
        }
    },
    "transportation": {
        "customID": {
            "id": "1146615565910016"
        },
        "onBehalfOfClient": {
            "companyId": "878518089023488",
            "companyName": "Virginia Black"
        },
        "organisation": {
            "departmentId": "8716975228321792",
            "departmentName": "Paul Sparks"
        },
        "requestType": "ACTUAL",
        "location": {
            "country": "Canada",
            "stateProvince": "YT",
            "zipPostCode": "R2E 8N2",
            "city": "Ewpihedi"
        },
        "site": {
            "siteId": "5694471998013440",
            "siteName": "Randy Barker",
            "buildingId": "7568795975548928",
            "buildingName": "Ruby Roberson"
        },
        "timePeriod": {
            "year": 2021,
            "month": 1
        },
        "activityData": {
            "typeOfActivityData": "Weight Distance",
            "vehicleType": "Road Vehicle - HGV - Articulated - Engine Size 3.5 - 33 tonnes",
            "distanceTravelled": "2000",
            "totalWeightOfFreight": "100",
            "numberOfPassengers": 15,
            "unitOfMeasurement": "Tonne Mile",
            "fuelUsed": "lahnajsizet",
            "fuelAmount": "5396432412475392",
            "unitOfFuelAmount": "2471533194772480"
        }
    }
}

# ================================
# API Configuration
# ================================
API_KEY = "PHXMWwqmY3vOemKDLf2cDNFbCviqKiBYRTmVNUFT44qYZQ"
BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJENDA5QTlBNjc1MzhBOTU0QUFDRjMyMkU1NjZDNENGOUZENkNBMzIiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJMVUNhbW1kVGlwVktyUE1pNVdiRXo1X1d5akkifQ.eyJuYmYiOjE3NDI2NDk3NTgsImV4cCI6MTc0MjY1MzM1OCwiaXNzIjoiaHR0cHM6Ly9hdXRoLWIyYi10d2MuaWJtLmNvbSIsImF1ZCI6WyJhY2Nlc3M6YWdybyIsImlibS1wYWlycy1hcGkiLCJwaG9lbml4LWFwaSJdLCJjbGllbnRfaWQiOiJpYm0tYWdyby1hcGkiLCJzdWIiOiI0MDc0YjQ2MS1mZDVhLTQxMjQtOTQxNy0yYTRmZDc3ZDEyZWEiLCJhdXRoX3RpbWUiOjE3NDI2NDk3NTgsImlkcCI6ImxvY2FsIiwiYXBwbGljYXRpb25zIjoiW1wiQUdST19BUElcIixcIkNBUkJPTl9BUElcIl0iLCJyb2xlcyI6Ilt7XCJhcHBsaWNhdGlvbklkXCI6XCJDQVJCT05fQVBJXCIsXCJyb2xlc1wiOltcIkFETUlOXCJdfV0iLCJhY2NvdW50IjoiOGIxNjA3YmMtODhkMC00ODU2LWI3NDUtMWNhMWQzNjBhMzEzIiwiYWNjb3VudF9uYW1lIjoiZWktcHJldmlldy12Mi03NzA2MmUxZi0wM2I3LTQ1ODAtYWJiYS01MjI3OTdjNjJhZDkiLCJzY29wZSI6WyJjdXN0b20ucHJvZmlsZSIsImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSIsImFjY2VzczphZ3JvIiwiaWJtLXBhaXJzLWFwaSIsInBob2VuaXgtYXBpIl0sImFtciI6WyJhcGlrZXkiXX0.qDCy0cO7fXPmyUTpNfJE7UaioE9wRuW5ELGZu-QMZVgvx1lQX8_iTUzWYiWKpeUrOIXvCkcuxYmABGd75eeYDi-2Ry43EgLP0xSZluU6XS6aOeGU69DCB2KQZVRpdDfiVNfM_3PFeTKpvbF1PH4aoOVt4bjaK08dirfQ95iinGfhWmPMZ2-A6tw_QO35k_mYjwaV2jGMkVjKNsd5BqShOyyqC9N7Cyci56N9KV96gepOoZ13cjqUGF2NbNX73oNp21RtDg0_JBWfJrQ8wKJrJQ65FCztsU5R5IOqQKBz6KiMgr-OWBBtFBt_EQEsAB-rugeeWgmqfBM4VkNjhZY8Hw"
BASE_URL = "https://foundation.agtech.ibm.com/v2"

API_ENDPOINTS = {
    "stationary": "/carbon/stationary",
    "fugitive": "/carbon/fugitive",
    "mobile": "/carbon/mobile",
    "transportation": "/carbon/transportation_and_distribution"
}

# ================================
# CSV Data Folder
# ================================
DATA_FOLDER = "csv_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# ================================
# Home Route
# ================================
@app.route('/')
def index():
    """Render the homepage with endpoint options."""
    return render_template('index.html', endpoints=API_ENDPOINTS)


# ================================
# Form Route
# ================================
@app.route('/form/<endpoint_type>')
def show_form(endpoint_type):
    """Show form with pre-filled JSON template"""
    if endpoint_type not in TEMPLATES:
        flash("Invalid API type.")
        return redirect(url_for('index'))

    return render_template('form.html', endpoint_type=endpoint_type, template_json=json.dumps(TEMPLATES[endpoint_type], indent=2))


# ================================
# Submit Form and Make API Call
# ================================
@app.route('/submit/<endpoint_type>', methods=['POST'])
def submit_form(endpoint_type):
    """Submit API request and store data"""
    if endpoint_type not in API_ENDPOINTS:
        flash("Invalid endpoint selected.")
        return redirect(url_for('index'))

    try:
        json_data = request.form.get('json_data', '{}')
        data = json.loads(json_data)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'apikey': API_KEY,
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

        api_url = f"{BASE_URL}{API_ENDPOINTS[endpoint_type]}"
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            result = response.json()
        else:
            result = {"error": "API request failed", "status_code": response.status_code, "response": response.text}

        csv_filename = f"{DATA_FOLDER}/{endpoint_type}_data.csv"
        save_response_to_csv(endpoint_type, data, result, csv_filename)

        # Send data and visualization parameters to result.html
        return render_template(
            'result.html',
            endpoint_type=endpoint_type,
            request_data=json.dumps(data, indent=2),
            result=json.dumps(result, indent=2)
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/convert_json_to_csv', methods=['POST'])
def convert_json_to_csv():
    """Convert user-provided JSON to CSV."""
    try:
        json_data = request.json
        csv_filename = f"{DATA_FOLDER}/custom_data.csv"

        # Convert JSON to CSV
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=json_data[0].keys())
            writer.writeheader()
            writer.writerows(json_data)

        return jsonify({"message": "JSON successfully converted to CSV!", "file": csv_filename})

    except Exception as e:
        return jsonify({"error": str(e)})


# ================================
# Save API Response to CSV
# ================================
def save_response_to_csv(endpoint_type, request_data, response_data, csv_filename):
    """Save API response with timestamp to a CSV"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    row = {
        'timestamp': timestamp,
        'request_data': json.dumps(request_data),
        'response_data': json.dumps(response_data)
    }

    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# ================================
# Download CSV Route
# ================================
@app.route('/download/<endpoint_type>')
def download_csv(endpoint_type):
    """Download stored API CSV data."""
    csv_filename = f"{DATA_FOLDER}/{endpoint_type}_data.csv"

    if os.path.exists(csv_filename):
        return send_file(csv_filename, as_attachment=True, download_name=f"{endpoint_type}_data.csv")
    else:
        flash(f"No data available for {endpoint_type} API.")
        return redirect(url_for('index'))


# ================================
# Run Flask App
# ================================
if __name__ == '__main__':
    app.run(debug=True)
