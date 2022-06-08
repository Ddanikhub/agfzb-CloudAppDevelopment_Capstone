import sys
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import Document, CloudantV1


Params = {
"review": 
    {
        "id": 1114,
        "name": "Upkar Lidder",
        "dealership": 1,
        "review": "Great service!",
        "purchase": True,
        "another": "field",
        "purchase_date": "02/16/2021",
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021
    }
}



def main(dict):
    authenticator = IAMAuthenticator( "qs-CR3c-ww_auqxziy-3Bp1pjh9FURpTvVP1Fmuwopds" )

    service = CloudantV1(authenticator=authenticator)

    service.set_service_url("https://705b1830-7b57-47a9-bc15-86ca8fee12fb-bluemix.cloudantnosqldb.appdomain.cloud")
 
    db_name = "reviews"

    
    response = service.post_document(db=db_name, document=dict["review"]).get_result()
    try:
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result    
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }




main(Params)
