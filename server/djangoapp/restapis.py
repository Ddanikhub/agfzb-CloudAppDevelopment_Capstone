from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
import requests
import json

from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    #print(kwargs)
    print("GET from {} ".format(url))
    json_data={}
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        #print(json_data)
    except Exception as e:
        print("Error " ,e)
    
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["allDocs"]["doc"]
        #print(dealers)
        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
#Coding practice: create a get_dealer_by_id or get_dealers_by_state method in restapis.py. HINT, the only difference from the get_dealers_from_cf method is adding a dealer id or state URL parameter argument when calling the def get_request(url, **kwargs): method such as get_request(url, dealerId=dealerId).


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerID):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerID=dealerID)
    #print(json_result)
 
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        # For each review object
        for review in reviews:
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_review_sentiments(review["review"]),
                id=review['id']
                )
            results.append(review_obj)
    #print(results[0])
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview, **kwargs):
    API_KEY="VtZwa_Wx_ZskF-u4wHuQ7pEuwYDEntsSg-5Ens9AM_hX"
    #API_KEY="0614ccd0-1e9f-4d49-923e-e7741f963747:Q3ZX2R1b3oBEb0XebEO99rpulJ31yoY7X5GfjoQykN4RpM9eThYrrs14If0aOHtG"
    NLU_URL='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/6a8b64d0-26f5-40da-b63f-641c0d439eca/v1/analyze?version=2020-08-01'
    params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
    response = requests.post(NLU_URL,data=params,headers={'Content-Type':'application/json'},auth=HTTPBasicAuth("apikey", API_KEY))
    
    #print(response.json())
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"

