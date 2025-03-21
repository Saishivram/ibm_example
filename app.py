from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
import requests
import json
import os

app = Flask(__name__)
app.secret_key = "ibm_environmental_intelligence_app_secret"

# IBM Environmental Intelligence API credentials
API_KEY = "PHXMWwqmY3vOemKDLf2cDNFbCviqKiBYRTmVNUFT44qYZQ"
BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJENDA5QTlBNjc1MzhBOTU0QUFDRjMyMkU1NjZDNENGOUZENkNBMzIiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJMVUNhbW1kVGlwVktyUE1pNVdiRXo1X1d5akkifQ.eyJuYmYiOjE3NDI1NTMyMzQsImV4cCI6MTc0MjU1NjgzNCwiaXNzIjoiaHR0cHM6Ly9hdXRoLWIyYi10d2MuaWJtLmNvbSIsImF1ZCI6WyJhY2Nlc3M6YWdybyIsImlibS1wYWlycy1hcGkiLCJwaG9lbml4LWFwaSJdLCJjbGllbnRfaWQiOiJpYm0tYWdyby1hcGkiLCJzdWIiOiI0MDc0YjQ2MS1mZDVhLTQxMjQtOTQxNy0yYTRmZDc3ZDEyZWEiLCJhdXRoX3RpbWUiOjE3NDI1NTMyMzQsImlkcCI6ImxvY2FsIiwiYXBwbGljYXRpb25zIjoiW1wiQUdST19BUElcIixcIkNBUkJPTl9BUElcIl0iLCJyb2xlcyI6Ilt7XCJhcHBsaWNhdGlvbklkXCI6XCJDQVJCT05fQVBJXCIsXCJyb2xlc1wiOltcIkFETUlOXCJdfV0iLCJhY2NvdW50IjoiOGIxNjA3YmMtODhkMC00ODU2LWI3NDUtMWNhMWQzNjBhMzEzIiwiYWNjb3VudF9uYW1lIjoiZWktcHJldmlldy12Mi03NzA2MmUxZi0wM2I3LTQ1ODAtYWJiYS01MjI3OTdjNjJhZDkiLCJzY29wZSI6WyJjdXN0b20ucHJvZmlsZSIsImVtYWlsIiwib3BlbmlkIiwicHJvZmlsZSIsImFjY2VzczphZ3JvIiwiaWJtLXBhaXJzLWFwaSIsInBob2VuaXgtYXBpIl0sImFtciI6WyJhcGlrZXkiXX0.bxmQiJKMoDCDzV7_ixg_9jznSY1vesrAIqso2qHDIeG0x-I0tWOskAvELJ7dh5VSlvQlDb55sN9kn0cjq7eiRn5Fpi0p6e8OBvDeaLwcXLtlWuvRcfpk_ghMmfUuNwXxdby27oF4AAJY8uoEPQQZrH0OAIVkid3E-29Ekox7ZPPMA5aHei4VKlkwTIlhfSmsBoV_Xy87puFLM9utkpJ3EoVMxKEOD9aAOylIZ0o3Y1632hwjlc4LoIMEC6VW91WdmZF6_MiMKLJg47WGUd-uFz2-jmA1G84_SYFFrT_M8uYT7Z4ZnXsnAJ_ryRUgAo9zCvUVqMwep4PYl7cdTxlUug"
BASE_URL = "https://foundation.agtech.ibm.com/v2"

# API endpoints
API_ENDPOINTS = {
    "stationary": "/carbon/stationary",
    "fugitive": "/carbon/fugitive",
    "mobile": "/carbon/mobile",
    "transportation": "/carbon/transportation_and_distribution"
}

@app.route('/')
def index():
    return render_template('index.html', endpoints=API_ENDPOINTS)

@app.route('/form/<endpoint_type>')
def show_form(endpoint_type):
    if endpoint_type not in API_ENDPOINTS:
        flash("Invalid endpoint type")
        return redirect(url_for('index'))
    
    # Create sample JSON templates based on the endpoint type
    # These are simplified examples and should be customized based on IBM's documentation
    templates = {
        "stationary": {
  "customID": {
    "id": "1341298940313600"
  },
  "onBehalfOfClient": {
    "companyId": "3963663115354112",
    "companyName": "Kathryn Fields"
  },
  "organisation": {
    "departmentId": "5095141542985728",
    "departmentName": "Mollie Schultz"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Puerto Rico",
    "stateProvince": "YT",
    "zipPostCode": "A0K 4G6",
    "city": "Suacelep"
  },
  "site": {
    "siteId": "2003616447594496",
    "siteName": "Richard Nguyen",
    "buildingId": "6884675171647488",
    "buildingName": "Philip Goodwin"
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
    "id": "7577466644201472"
  },
  "onBehalfOfClient": {
    "companyId": "6298454785523712",
    "companyName": "Angel Hodges"
  },
  "organisation": {
    "departmentId": "1735992104976384",
    "departmentName": "Belle Horton"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Russian Federation",
    "stateProvince": "YT",
    "zipPostCode": "G5O 5F9",
    "city": "Ofmokuw"
  },
  "site": {
    "siteId": "4238989278052352",
    "siteName": "Randy Arnold",
    "buildingId": "2104636035039232",
    "buildingName": "Angel Little"
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
    "id": "8628876682985472"
  },
  "onBehalfOfClient": {
    "companyId": "7013878609215488",
    "companyName": "Tommy Schneider"
  },
  "organisation": {
    "departmentId": "8580177393090560",
    "departmentName": "Nancy Ferguson"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Ethiopia",
    "stateProvince": "NB",
    "zipPostCode": "R9N 6P3",
    "city": "Cohirgap"
  },
  "site": {
    "siteId": "2237449315024896",
    "siteName": "Ethel Weber",
    "buildingId": "8926667875549184",
    "buildingName": "Lina Moreno"
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
    "id": "5071445279375360"
  },
  "onBehalfOfClient": {
    "companyId": "655382647144448",
    "companyName": "Jason Stokes"
  },
  "organisation": {
    "departmentId": "3094281365487616",
    "departmentName": "Elnora Ballard"
  },
  "requestType": "ACTUAL",
  "location": {
    "country": "Zimbabwe",
    "stateProvince": "PE",
    "zipPostCode": "N9R 3Z8",
    "city": "Vamdikit"
  },
  "site": {
    "siteId": "7273159032045568",
    "siteName": "Nathaniel Martinez",
    "buildingId": "395364999888896",
    "buildingName": "Luke Doyle"
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
    "fuelUsed": "ufiinokidhepah",
    "fuelAmount": "2140997402230784",
    "unitOfFuelAmount": "2161481175007232"
  }
}
    }
    
    return render_template('form.html', 
                           endpoint_type=endpoint_type, 
                           template_json=json.dumps(templates[endpoint_type], indent=2))

@app.route('/submit/<endpoint_type>', methods=['POST'])
def submit_form(endpoint_type):
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
            'x-ibm-client-id': API_KEY,
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
        
        # Construct the full API URL
        api_url = f"{BASE_URL}{API_ENDPOINTS[endpoint_type]}"
        
        # Make the API request
        response = requests.post(api_url, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code in (200, 201, 202):
            try:
                result = response.json()
            except:
                result = {"raw_response": response.text}
        else:
            result = {
                "error": "API request failed",
                "status_code": response.status_code,
                "response": response.text
            }
        
        return render_template('result.html', 
                              endpoint_type=endpoint_type,
                              request_data=json.dumps(data, indent=2),
                              result=json.dumps(result, indent=2))
    
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)