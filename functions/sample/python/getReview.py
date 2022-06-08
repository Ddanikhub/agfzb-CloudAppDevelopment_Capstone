import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

dealerID = {"dealership": {"15"}}



def main(dict):
    authenticator = IAMAuthenticator( "qs-CR3c-ww_auqxziy-3Bp1pjh9FURpTvVP1Fmuwopds" )

    service = CloudantV1(authenticator=authenticator)

    service.set_service_url("https://705b1830-7b57-47a9-bc15-86ca8fee12fb-bluemix.cloudantnosqldb.appdomain.cloud")
 
    db_name = "reviews"
    
    response = service.post_find(
        db=db_name,
        selector={'dealership': {'$eq': int(dict["dealerID"])}},
        fields=["_id", "_rev", "id", "name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
        ).get_result()
    try:   
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        print(result)
        return(result)
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
        


main(dealerID)


# try:
#         response = service.post_all_docs(
#             db='reviews',
#             include_docs=True,
#         ).get_result()
#     except ApiException as ae:
#         print("Method failed")
#         print(" - status code: " + str(ae.code))
#         print(" - error message: " + ae.message)
#         if ("reason" in ae.http_response.json()):
#             print(" - reason: " + ae.http_response.json()["reason"])
#     finally:
#         return(response)


 #   selector={'dealership': {'&eq': int(dict['dealerID'])}},
          #  selector= {"dealership": int(dict["dealership"])},
         #   selector={'dealership': {'$eq': dict['dealerId']}},
         #   selector={'dealership': {'$eq': select}},

         
  #  select = dict
  #  print(select)
  #  select["dealership"] = int(select["dealership"])
 #   print(select)
 #   select = dict["dealerID"]
    #print(dict) 

# 3. Get database information