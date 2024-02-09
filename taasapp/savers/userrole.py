from ..models import UserRole
from ..serializers import SaveUserRoleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.db import connection
from ..utils import dictfetchall
class SaveUsersRoleView(APIView):
    serializer_class =SaveUserRoleSerializer
    #permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=SaveUserRoleSerializer)
    
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveUserRoleSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                
                username_check = UserRole.objects.filter(username = request.data['username'],roleID =request.data["roleID"])
                if(username_check):
                    return Response({"error":"Role already assigned","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                      
                serializer.save()
                usersCount = UserRole.objects.filter(userID = request.data["userID"]).count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':usersCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request, id=None):
         if request.method == 'GET':
             try:       
                    userRecord = UserRole.objects.filter(userID =id)
                    serializer = SaveUserRoleSerializer(userRecord, many=True)
                    return Response({'message':'FETCH_SUCCESS','data':serializer.data}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
class ListUserRolesView(APIView):
       def get(self, request, *args, id=None):
         if request.method == 'GET':
            try:   
                with connection.cursor() as cursor:
                    #cursor.callproc("test_procedure", [1, "test"])
                    cursor.execute("SELECT taasapp_userrole.*, taasapp_roles.id AS roleid, taasapp_roles.name  FROM taasapp_userrole INNER JOIN taasapp_roles ON taasapp_userrole.id = taasapp_roles.id  WHERE taasapp_userrole.username = %s", [id])
                    results = dictfetchall(cursor)
                return Response({'message':'FETCH_SUCCESS','data':results}) 
            except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  