from flask import Flask
from flask import request
from flask import make_response
from google.cloud import bigquery

import json
import os
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='mayabot_admin.json'


# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)

    print(json.dumps(req, indent=4))

    res = makeResponse(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
def makeResponse(req):

    result = req.get("queryResult")

    speech = "something went wrong"

    action = result.get("action")

    if action == "bookcar":
        parameters = result.get("parameters")

        city = parameters.get("geo-city")
        date = parameters.get("date")
        cars = parameters.get("cars")
    
        print(f"city is {city} and date is {date} and cars type is {cars}")
        print(f"action is {action}")
        BigQuery_client = bigquery.Client()
        query = "SELECT name[SAFE_OFFSET(0)] FROM `steel-signifier-364303.maya_data.Patient`"
        query_job = BigQuery_client.query(query)

        for row in query_job.result():
            print(row)
        
        speech = f"city is {city} and date is {date} and cars type is {cars} and row is {row}"



    return {"fulfillmentMessages":[
        {
            "text":{
                "text":[speech]
            }
        }]}

    # return {
    # "speech": speech,
    # "displayText": speech,
    # "source": "apiai-weather-webhook"
    # }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
