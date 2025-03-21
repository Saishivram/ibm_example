from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_cors import CORS  # Import CORS
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "ibm_environmental_intelligence_app_secret"
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# IBM Environmental Intelligence API credentials
API_KEY = "PHXMWwqmY3vOemKDLf2cDNFbCviqKiBYRTmVNUFT44qYZQ"
BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJENDA5QTlBNjc1MzhBOTU0QUFDRjMyMkU1NjZDNENGOUZENkNBMzIiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJMVUNhbW1kVGlwVktyUE1pNVdiRXo1X1d5akkifQ.eyJuYmYiOjE3NDI1NjE0MzcsImV4cCI6MTc0MjU2NTAzNywiaXNzIjoiaHR0cHM6Ly9hdXRoLWIyYi10d2MuaWJtLmNvbSIsImF1ZCI6WyJhY2Nlc3M6YWdybyIsImlibS1wYWlycy1hcGkiLCJwaG9lbml4LWFwaSJdLCJjbGllbnRfaWQiOiJpYm0tYWdyby1hcGkiLCJzdWIiOiI0MDc0YjQ2MS1mZDVhLTQxMjQtOTQxNy0yYTRmZDc3ZDEyZWEiLCJhdXRoX3RpbWUiOjE3NDI1NjE0MzcsImlkcCI6ImxvY2FsIiwiYXBwbGljYXRpb25zIjoiW1wiQUdST19BUElcIixcIkNBUkJPTl9BUElcIl0iLCJyb2xlcyI6Ilt7XCJhcHBsaWNhdGlvbklkXCI6XCJDQVJCT05fQVBJXCIsXCJyb2xlc1wiOltcIkFETUlOXCJdfV0iLCJhY2NvdW50IjoiOGIxNjA3YmMtODhkMC00ODU2LWI3NDUtMWNhMWQzNjBhMzEzIiwiYWNjb3VudF9uYW1lIjoiZWktcHJldmlldy12Mi03NzA2MmUxZi0wM2I3LTQ1ODAtYWJiYS01MjI3OTdjNjJhZDkiLCJzY29wZSI6WyJjdXN0b20ucHJvZmlsZSIsImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSIsImFjY2VzczphZ3JvIiwiaWJtLXBhaXJzLWFwaSIsInBob2VuaXgtYXBpIl0sImFtciI6WyJhcGlrZXkiXX0.NT9_6JHcSuY7Jki1Ft8rtDIy8kaKeeVLsiwdE6nsMUhVP0eLZs2n8hrLVZhD7Y3ECo0UILXZjLO9MFicrDhshRT65WtsHPcyXj50uQbH14yuI4GIp8gZsv2L3XMwl20jHYHXqw08VfKT6TxXBrjXtz4cVXZsA5bzp0bii9ivLuROLWJHB5aemkgzIwUBQSDC6NF3uEP6st-q159YW79ouzQXAbrsA0-GcjWCt09mqkYFb0pj28_lo8B5ocB-Uew0EwxmYfo31gzWtYctUw284J4M0dYf9w3UWUsaPkvjM-1jT6LvULEI9IYHOVYRfHBYSeMDb0oGfPsiLD3Ec2eKtw"  # Replace with a valid token
BASE_URL = "https://foundation.agtech.ibm.com/v2"

# API endpoints
API_ENDPOINTS = {
    "stationary": "/carbon/stationary",
    "fugitive": "/carbon/fugitive",
    "mobile": "/carbon/mobile",
    "transportation": "/carbon/transportation_and_distribution"
}

# ===============================
# API Health Check Route
# ===============================
@app.route('/status')
def check_api_status():
    """Check API Status"""
    status_url = f"{BASE_URL}/status"
    headers = {
        'Accept': 'application/json',
        'apikey': API_KEY
    }

    try:
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            return jsonify({"status": "API is accessible", "response": response.json()}), 200
        else:
            return jsonify({"error": "API is not accessible", "status_code": response.status_code, "response": response.text}), 403
    except requests.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500


# ===============================
# Home Route
# ===============================
@app.route('/')
def index():
    return render_template('index.html', endpoints=API_ENDPOINTS)


# ===============================
# Form Route
# ===============================
@app.route('/form/<endpoint_type>')
def show_form(endpoint_type):
    """Show form based on endpoint type"""
    if endpoint_type not in API_ENDPOINTS:
        flash("Invalid endpoint type")
        return redirect(url_for('index'))

    # Sample JSON templates
    templates = {
        "stationary": {
  "customID": {
    "id": "3942881448427520"
  },
  "onBehalfOfClient": {
    "companyId": "595774406656000",
    "companyName": "Rachel Moran"
  },
  "organisation": {
    "departmentId": "2230610022105088",
    "departmentName": "Scott Green"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Sri Lanka",
    "stateProvince": "YT",
    "zipPostCode": "X3S 8K5",
    "city": "Vownijtir"
  },
  "site": {
    "siteId": "3153998422999040",
    "siteName": "Catherine Chambers",
    "buildingId": "8817844590477312",
    "buildingName": "Lora Reed"
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
    "id": "6362669906919424"
  },
  "onBehalfOfClient": {
    "companyId": "2101010115854336",
    "companyName": "Bryan Wagner"
  },
  "organisation": {
    "departmentId": "4478310591496192",
    "departmentName": "Catherine Welch"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Burkina Faso",
    "stateProvince": "NU",
    "zipPostCode": "C4A 8N9",
    "city": "Givevuole"
  },
  "site": {
    "siteId": "6581270588948480",
    "siteName": "Effie Hunt",
    "buildingId": "5048841520807936",
    "buildingName": "Emily Soto"
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
    "id": "3199472771268608"
  },
  "onBehalfOfClient": {
    "companyId": "2919865377619968",
    "companyName": "Nannie Gill"
  },
  "organisation": {
    "departmentId": "1769042236932096",
    "departmentName": "Iva Grant"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Saint Kitts and Nevis",
    "stateProvince": "AB",
    "zipPostCode": "P6Z 7J9",
    "city": "Bimbanzid"
  },
  "site": {
    "siteId": "4785532812918784",
    "siteName": "Landon Lynch",
    "buildingId": "1579188448395264",
    "buildingName": "Daisy Fleming"
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
    "id": "6546727051984896"
  },
  "onBehalfOfClient": {
    "companyId": "1323470287798272",
    "companyName": "Jackson Todd"
  },
  "organisation": {
    "departmentId": "705312396935168",
    "departmentName": "Blake Oliver"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "South Georgia and the South Sandwich Islands",
    "stateProvince": "NU",
    "zipPostCode": "S1D 9G5",
    "city": "Tehentu"
  },
  "site": {
    "siteId": "3622584685953024",
    "siteName": "Edith Kelly",
    "buildingId": "3289033870409728",
    "buildingName": "Mae Dean"
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
    "fuelUsed": "zumz",
    "fuelAmount": "2856980838350848",
    "unitOfFuelAmount": "5942904646270976"
  }
}
    }

    return render_template('form.html', endpoint_type=endpoint_type, template_json=json.dumps(templates[endpoint_type], indent=2))


# ===============================
# Submit Form and Make API Call
# ===============================
@app.route('/submit/<endpoint_type>', methods=['POST'])
def submit_form(endpoint_type):
    """Submit form and call API"""
    if endpoint_type not in API_ENDPOINTS:
        return jsonify({"error": "Invalid endpoint type"}), 400

    try:
        # Get the JSON data from the form
        json_data = request.form.get('json_data', '{}')
        data = json.loads(json_data)

        # Prepare headers with authentication
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'apikey': API_KEY,
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

        # Construct the full API URL
        api_url = f"{BASE_URL}{API_ENDPOINTS[endpoint_type]}"

        # Debugging: Print request details
        print("Request URL:", api_url)
        print("Headers:", headers)
        print("Payload:", json.dumps(data, indent=2))

        # Make the API request
        response = requests.post(api_url, json=data, headers=headers)

        # Debugging: Print API response
        print("Response Status:", response.status_code)
        print("Response Text:", response.text)

        # Check if the request was successful
        if response.status_code in (200, 201, 202):
            try:
                result = response.json()
            except json.JSONDecodeError:
                result = {"raw_response": response.text}
        else:
            result = {
                "error": "API request failed",
                "status_code": response.status_code,
                "response": response.text
            }

        return render_template('result.html', endpoint_type=endpoint_type, request_data=json.dumps(data, indent=2), result=json.dumps(result, indent=2))

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# Run Flask Application
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
