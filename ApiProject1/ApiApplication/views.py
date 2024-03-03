from django.http import HttpResponse, JsonResponse 
from bson import ObjectId  
from django.views import View 
from .models import db_user_collection,db_sessions_colletion
import json
from django.views.decorators.csrf import csrf_exempt 
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password
from datetime import datetime

def index(request):
    return JsonResponse({"message": "App is running"}, status=200)  

############################################################################################################

@method_decorator(csrf_exempt, name='dispatch')
class login(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            emailid = data.get('emailid')
            password = data.get('password')
            userdata = db_user_collection.find_one({"emailid": emailid})
            if userdata:
                stored_password = userdata.get('password')
                if password==stored_password:
                    userdata['_id'] = str(userdata['_id'])
                    return JsonResponse({"message": "success", "userdata":userdata}, status=200)
                else:
                    return JsonResponse({"message": "Password does not match"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)

############################################################################################################
            # _id:65cdfe1c3fa2f1dc1a041ff2
            # firstname:"ram"
            # lastname:"p"
            # emailid:"ram@gmail.com"
            # password:"password"
            # sessions:Array (1)
            # images:Array (1)

@method_decorator(csrf_exempt, name='dispatch')
class AddUser(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            emailid = data.get('emailid')
            password = data.get('password')
            mobileno = data.get('mobileno')
            existing_user = db_user_collection.find_one({"emailid": emailid})

            if existing_user is not None:
                return JsonResponse({"error": "Account already exists with this email id"}, status=400)

            record = {
                "firstname": firstname,
                "lastname": lastname,
                "emailid" : emailid,
                "mobileno":mobileno,
                "password" : password,
                "sessions" : [],
                "images" : []
            }
            print(record)
            db_user_collection.insert_one(record)
            userdata = getUserDataForRegisteration(emailid)
            userdata['_id'] = str(userdata['_id'])
            return JsonResponse({"message": "success", "data": userdata}, status=200) 
        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)

#######################################################################################

def get_data(request):
    try:
        data = list(db_user_collection.find())
        data = list(map(lambda doc: {**doc, '_id': str(doc['_id'])}, data))
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500) 


##########################          convert timestamp to date              ###############################

# # Assuming the timestamp value is stored in a variable called 'timestamp_value'
# timestamp_value = 1708338020

# # Convert the timestamp to a datetime object
# datetime_obj = datetime.fromtimestamp(timestamp_value)

# # Print the date and time
# print("Converted Date and Time:", datetime_obj)
############################################################################################################

@method_decorator(csrf_exempt, name='dispatch')
class generateImage(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            userid = data.get('_id')
            if userid:
                userdata = CHECKIFUSEREXISTS(userid)
                if userdata and userdata.get('_id'):
                    return JsonResponse({"message": "this is test generated image"}, status=200)
                else:
                    return JsonResponse({"message": "user error "}, status=300)
            else:
                return JsonResponse({"message": "error : userid empty !!!"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)

############################################################################################################

@method_decorator(csrf_exempt, name='dispatch')
class getUserProfile(View):
    def post(self, request):
        try:
            print("hi")
            data = json.loads(request.body)
            userid = data.get('_id')
            if userid:
                userdata = CHECKIFUSEREXISTS(userid)
                if userdata:
                    userdata['_id'] = str(userdata['_id'])
                    print(userdata)
                    return JsonResponse({"userdata": userdata}, status=200)
                else:
                    return JsonResponse({"error": "User not found"}, status=404)
            else:
                return JsonResponse({"error": "User ID not provided"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error occurred: {str(e)}"}, status=500)         

############################################################################################################

def CHECKIFUSEREXISTS(userid):
    userid = ObjectId(userid)
    userdata = db_user_collection.find_one({"_id": userid})
    return userdata

#############################################

def getUserDataForRegisteration(emailid):
    userdata = db_user_collection.find_one({"emailid": emailid})
    return userdata

###########################################################################################################
def test_endpoint(request):
    return JsonResponse({'message': 'Django backend connected successfully!'},status=200)    