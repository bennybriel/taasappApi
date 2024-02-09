from ..models import Permissions
from ..serializers import SavePermissionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema

class SavePermissionsView(APIView):
    serializer_class =SavePermissionSerializer
    @swagger_auto_schema(request_body=SavePermissionSerializer)
    def post(self, request):
        if request.method == 'POST':
            serializer = SavePermissionSerializer(data=request.data)
        try:
            if serializer.is_valid():
                
                name_check = Permissions.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
             
                if(name_check):
                    return Response({"error":"Permission already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                              
                serializer.save()
                permissionCount = Permissions.objects.filter(userID = request.data['userID']).count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':permissionCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request,id=None):
         if request.method == 'GET':
             permissionCountRecord = Permissions.objects.filter(userID=id)
             return Response({'message':'SAVED_SUCCESS','data':list(permissionCountRecord.values())}) 
             
           
        