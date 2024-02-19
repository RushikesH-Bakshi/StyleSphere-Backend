from django.http import HttpResponse, JsonResponse 
from bson import ObjectId  
from django.views import View 
from .models import db_user_collection,db_sessions_colletion
import json
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator

def index(request):
    return JsonResponse({"message": "App is running"})  


            # _id:65cdfe1c3fa2f1dc1a041ff2
            # firstname:"ram"
            # lastname:"p"
            # emailid:"ram@gmail.com"
            # password:"password"
            # sessions:Array (1)
            # images:Array (1)

@method_decorator(csrf_exempt, name='dispatch')
class AddUserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            emailid = data.get('emailid')
            password = data.get('password')

            # Check if emailid already exists in the database
            existing_user = db_user_collection.find_one({"emailid": emailid})

            if existing_user is not None:
                existing_user['_id'] = str(existing_user['_id'])
                return JsonResponse({"error": "Account already exists with this email id"}, status=400)

            # Insert the new record
            record = {
                "firstname": firstname,
                "lastname": lastname,
                "emailid" : emailid,
                "password" : password,
                "sessions" : [],
                "images" : []
            }
            db_user_collection.insert_one(record)
            
            return JsonResponse({"message": "New record added"}) 
        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)

def get_data(request):
    try:
        data = list(db_user_collection.find())
        data = list(map(lambda doc: {**doc, '_id': str(doc['_id'])}, data))
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500) 


##########################          convert timestamp to date              ###############################
# from datetime import datetime

# # Assuming the timestamp value is stored in a variable called 'timestamp_value'
# timestamp_value = 1708338020

# # Convert the timestamp to a datetime object
# datetime_obj = datetime.fromtimestamp(timestamp_value)

# # Print the date and time
# print("Converted Date and Time:", datetime_obj)
############################################################################################################
