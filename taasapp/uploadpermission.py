import csv
from .models import Users
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import io  # Add this import
from io import TextIOWrapper
def isfileuploadpermission(userID):
   try:
        check = Users.objects.filter(userID=userID)
        if not check.exists():
            return False
        return True
   except:
        return False
