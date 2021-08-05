import os
from flask import Flask, render_template
from dotenv import load_dotenv
import requests
from apiKey import api_Key_yelp
from apiKey import api_Key_location
from flask import request


load_dotenv()
app = Flask(__name__)

# API #1
ENDPOINT_IP = "https://api.ipify.org?format=json"  # method: GET
response_ip = requests.get(url=ENDPOINT_IP)
ip = response_ip.json()["ip"] # ip now stores your ip

# API #2
API_KEY_LOC = api_Key_location  # for ipstack
# ENDPOINT_LOC = http://api.ipstack.com/
ENDPOINT_LOC = f"https://ipinfo.io/{ip}?token=e5705a55652e77"  # method: GET
response_loc = requests.get(url=ENDPOINT_LOC)

response_new = response_loc.json()['loc'].split(",")
lat, long = response_new[0], response_new[1]



client_id = "_yVwgo9pbZN4s883GVMXyg"
API_KEY_YELP= api_Key_yelp
ENDPOINT_YELP = "https://api.yelp.com/v3/businesses/search"  # method: GET
HEADERS_YELP = {"Authorization": "bearer %s" % API_KEY_YELP}


class user_category:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def repr(self):
        return self.type


# restaurants 
@app.route("/", methods=["GET", "POST"])
def index():
    testLocation = "toronto"
    category = "poop"
    if request.method == "POST":
        
        selection = request.form.get("type")
        S = user_category(selection, testLocation)
        category = S.repr()

    PARAMETERS_YELP = {
        "term": category,
        "limit": 50,
        "offset": 50,
        "radius": 10000,
        # "location": testLocation,  # CHANGE TO COORDINATES (LAT/LONG)
        "latitude": lat,
        "longitude": long,
    }

    response = requests.get(url=ENDPOINT_YELP, params=PARAMETERS_YELP, headers=HEADERS_YELP)
    business_data = response.json()
    print(business_data)

    # ENDPOINT_R = "https://api.yelp.com/v3/businesses/{id}/reviews"  # this doesnt work
    # response_R = requests.get(url=ENDPOINT_R, headers=HEADERS)
    # business_review = response_R.json()

    return render_template(
        "index.html",
        title="StreetEats",
        url=os.getenv("URL"),
        data=business_data,
        # review=business_review,
    )
