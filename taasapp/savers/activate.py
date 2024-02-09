from ..models import Users
from ..serializers import SchoolActivatorSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
import uuid
from drf_yasg.utils import swagger_auto_schema
from ..authenticateHeader import authenticate_user
class ActivateSchoolView(APIView):
    serializer_class =SchoolActivatorSerializer
    def post(self, request):
        if request.method == 'POST':
            try:
                authenticated, response = authenticate_user(request, request.data["userID"])
                # If authentication failed, return the response
                if not authenticated:
                        return response     
                # print(request.data) 
                # check  = Users.objects.filter(email =request.data["email"]).first()
               
                # if not check:
                #     return Response({"error":"Sorry User Not Authorized","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                user     = Users.objects.get(id=request.data["id"])
                user.status = request.data["status"]
                user.save()    
                # userCount = Users.objects.filter(userID = request.data["id"]).count()            
                return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':1, 
                                    'expireDate':datetime.datetime.now(),
                                    'message':'SAVED_SUCCESS',
                                    'statuscode':200,
                                    }, status=status.HTTP_200_OK)
               
            except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        return Response({'message':'SERVER_ERORR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
    # def get(self,request,id=None):
    #      if request.method == 'GET':
    #          userKey = Users.objects.filter(userID=id)
    #          return Response({'message':'SAVED_SUCCESS','data':list(userKey.values())}) 

        