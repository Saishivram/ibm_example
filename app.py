from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, send_file
from flask_cors import CORS
import requests
import json
import os
import csv

app = Flask(__name__)
app.secret_key = "ibm_environmental_intelligence_app_secret"
CORS(app, resources={r"/*": {"origins": "*"}})

# IBM Environmental Intelligence API credentials
API_KEY = "PHXMWwqmY3vOemKDLf2cDNFbCviqKiBYRTmVNUFT44qYZQ"
BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJENDA5QTlBNjc1MzhBOTU0QUFDRjMyMkU1NjZDNENGOUZENkNBMzIiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJMVUNhbW1kVGlwVktyUE1pNVdiRXo1X1d5akkifQ.eyJuYmYiOjE3NDI1Njk0OTEsImV4cCI6MTc0MjU3MzA5MSwiaXNzIjoiaHR0cHM6Ly9hdXRoLWIyYi10d2MuaWJtLmNvbSIsImF1ZCI6WyJhY2Nlc3M6YWdybyIsImlibS1wYWlycy1hcGkiLCJwaG9lbml4LWFwaSJdLCJjbGllbnRfaWQiOiJpYm0tYWdyby1hcGkiLCJzdWIiOiI0MDc0YjQ2MS1mZDVhLTQxMjQtOTQxNy0yYTRmZDc3ZDEyZWEiLCJhdXRoX3RpbWUiOjE3NDI1Njk0OTEsImlkcCI6ImxvY2FsIiwiYXBwbGljYXRpb25zIjoiW1wiQUdST19BUElcIixcIkNBUkJPTl9BUElcIl0iLCJyb2xlcyI6Ilt7XCJhcHBsaWNhdGlvbklkXCI6XCJDQVJCT05fQVBJXCIsXCJyb2xlc1wiOltcIkFETUlOXCJdfV0iLCJhY2NvdW50IjoiOGIxNjA3YmMtODhkMC00ODU2LWI3NDUtMWNhMWQzNjBhMzEzIiwiYWNjb3VudF9uYW1lIjoiZWktcHJldmlldy12Mi03NzA2MmUxZi0wM2I3LTQ1ODAtYWJiYS01MjI3OTdjNjJhZDkiLCJzY29wZSI6WyJjdXN0b20ucHJvZmlsZSIsImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSIsImFjY2VzczphZ3JvIiwiaWJtLXBhaXJzLWFwaSIsInBob2VuaXgtYXBpIl0sImFtciI6WyJhcGlrZXkiXX0.UQA0sn31qaDP40_JCDImo8No9GO5VM4TmYjjNTvkYp7anQ-e17pbsm8vT252XylfpcSZCPdexbxTBZMbaQX-dEyt6iuGfggCMzpn0-UQ1-uPYpEFbFq8IaIMs5JtZntirLhLZA0lUVO2N7HiWkDAFEZQ5NLf6PyaF5qfzua6NdMhAfiZ5PTywh-71gWFbIQrDpK2wsotGaKiUJi-dcmYi9o1JoQXivIPaYaPmIPd_vZ6Fir6bpB6GIW4s-ywtGT3O6qhOUm4blxEsfsvLOhSQRerSUS5uzUpbFa_Mj8tarkLnxQnfhVjY_LXBFv0DyaHgnGx1LBz4hLaPa8-Mws4Bg"
BASE_URL = "https://foundation.agtech.ibm.com/v2"

# API endpoints
API_ENDPOINTS = {
    "stationary": "/carbon/stationary",
    "fugitive": "/carbon/fugitive",
    "mobile": "/carbon/mobile",
    "transportation": "/carbon/transportation_and_distribution"
}

# CSV file for API responses
CSV_FILE = "api_responses.csv"

# ================================
# API Health Check Route
# ================================
@app.route('/status')
def check_api_status():
    """Check API Status"""
    status_url = f"{BASE_URL}/status"
    headers = {'Accept': 'application/json', 'apikey': API_KEY}

    try:
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            return jsonify({"status": "API is accessible", "response": response.json()}), 200
        else:
            return jsonify({"error": "API is not accessible", "status_code": response.status_code, "response": response.text}), 403
    except requests.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500


# ================================
# Home Route
# ================================
@app.route('/')
def index():
    return render_template('index.html', endpoints=API_ENDPOINTS)


# ================================
# Form Route
# ================================
@app.route('/form/<endpoint_type>')
def show_form(endpoint_type):
    """Show form based on endpoint type"""
    if endpoint_type not in API_ENDPOINTS:
        flash("Invalid endpoint type")
        return redirect(url_for('index'))

    # Sample JSON templates (kept for user modification)
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

    return render_template('form.html', endpoint_type=endpoint_type, template_json=json.dumps(TEMPLATES[endpoint_type], indent=2))


# ================================
# Submit Form and Make API Call
# ================================
@app.route('/submit/<endpoint_type>', methods=['POST'])
def submit_form(endpoint_type):
    """Submit form and call API"""
    if endpoint_type not in API_ENDPOINTS:
        return jsonify({"error": "Invalid endpoint type"}), 400

    try:
        # Get JSON data from form
        json_data = request.form.get('json_data', '{}')
        data = json.loads(json_data)

        # Prepare headers with authentication
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'apikey': API_KEY,
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

        # Construct API URL
        api_url = f"{BASE_URL}{API_ENDPOINTS[endpoint_type]}"

        # Make API request
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code in (200, 201, 202):
            result = response.json()
        else:
            result = {"error": "API request failed", "status_code": response.status_code, "response": response.text}

        # Save response to CSV
        save_response_to_csv(endpoint_type, data, result)

        return render_template('result.html', endpoint_type=endpoint_type, request_data=json.dumps(data, indent=2), result=json.dumps(result, indent=2))

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================
# Save API Response to CSV
# ================================
from datetime import datetime

def save_response_to_csv(endpoint_type, request_data, response_data):
    """Append API response to CSV with timestamp"""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csv_file:
        # Updated fieldnames to include 'timestamp'
        fieldnames = ['timestamp', 'endpoint_type', 'request_data', 'response_data']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if the file is newly created
        if not file_exists:
            writer.writeheader()

        # Generate current timestamp
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Write the new response with timestamp
        writer.writerow({
            'timestamp': current_timestamp,
            'endpoint_type': endpoint_type,
            'request_data': json.dumps(request_data),
            'response_data': json.dumps(response_data)
        })



# ================================
# Download CSV Route
# ================================
@app.route('/download_csv')
def download_csv():
    """Download the API response CSV"""
    return send_file(CSV_FILE, as_attachment=True, download_name="api_responses.csv")


# ================================
# Run Flask Application
# ================================
if __name__ == '__main__':
    app.run(debug=True)
