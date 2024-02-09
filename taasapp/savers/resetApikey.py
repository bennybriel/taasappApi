from ..models import Users,Apikeys
from ..serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
import uuid
from drf_yasg.utils import swagger_auto_schema
class ResetApiKeyView(APIView):
    serializer_class =UserSerializer
    def post(self,request):
        if request.method == 'POST':
            try:
                
                check  = Users.objects.filter(userID =request.data["userID"])
                print(request.data)
                if not check:
                    return Response({"error":"Sorry User Not Authorized","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                apikey1 = str(uuid.uuid4())
                apikey = apikey1
                user     = Apikeys.objects.get(userID=request.data["userID"])
                user.apikey = apikey
                user.isapiKey = True
                user.save()    
                userCount = Apikeys.objects.filter(userID = request.data["userID"]).count()            
                return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':userCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'apikey':apikey,
                                    'message':'SAVED_SUCCESS',
                                    'statuscode':200,
                                    }, status=status.HTTP_200_OK)
               
            except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        return Response({'message':'SERVER_ERORR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
    def get(self,request,id=None):
         if request.method == 'GET':
             userKey = Apikeys.objects.filter(userID=id)
             return Response({'message':'SAVED_SUCCESS','data':list(userKey.values())}) 

        