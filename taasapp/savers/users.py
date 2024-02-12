from ..models import Users
from ..serializers import UsersSerializer
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
from rest_framework.decorators import api_view
from ..authenticateHeader import authenticate_user

class SaveUsersView(APIView):
    serializer_class =UsersSerializer
    # permission_classes = []
    @swagger_auto_schema(request_body=UsersSerializer)
    
    def post(self, request):
        if request.method == 'POST':
            serializer = UsersSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                email_check = Users.objects.filter(email = request.data['email'])
                if(email_check):
                    return Response({"error":"Email already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
            
                username_check = Users.objects.filter(username = request.data['username'])
                if(username_check):
                    return Response({"error":"Username already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                phone_check = Users.objects.filter(phone = request.data['phone'])
                if(phone_check):
                    return Response({"error":"Phone already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
                
                serializer.save()
                usersCount = Users.objects.filter(userID = request.data["userID"]).count()
            
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
 
    def get(self, request, id=None):
         if request.method == 'GET':
             try:       
                    userRecord = Users.objects.filter(userID =id)
                    return Response({'message':'FETCH_SUCCESS','data':list(userRecord.values()),'statuscode':200}) 
                    #return Response({'message':'SERVER_ERORR','error':serializer.error, 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
class DeleteUsersView(APIView):
    
    def delete(self, request, id, format=None):
        try:
            
            instance = Users.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully", 'expireDate':datetime.datetime.now}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
      
        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    
class ListSchoolAccountView(APIView):
       def get(self, request, *args, id=None):
         if request.method == 'GET':
            try:   
                # authenticated, response = authenticate_user(request, id)
                # # If authentication failed, return the response
                # if not authenticated:
                #     return response                   
                              
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM  taasapp_users WHERE isschool='true'")
                    results = dictfetchall(cursor)
                return Response({'message':'FETCH_SUCCESS','data':results}) 
            except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
