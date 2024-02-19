from django.db import models
from ApiApplication.db_connection import db

# Create your models here.
db_user_collection=db['new']
db_sessions_colletion=db['sessions']