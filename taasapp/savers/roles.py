from ..models import Roles
from ..serializers import SaveRolesSerializer
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

class SaveRolesView(APIView):
    serializer_class =SaveRolesSerializer
    permission_classes = []
    @swagger_auto_schema(request_body=SaveRolesSerializer)
    
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveRolesSerializer(data=request.data)
        try:
            if serializer.is_valid():
          
              
                name_check = Roles.objects.filter(name = request.data['name']).filter(userID = request.data["userID"])
                
                if(name_check):
                    return Response({"error":"Name already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                serializer.save()
                rolesCount = Roles.objects.filter(userID = request.data["userID"]).count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':rolesCount, 
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
                    rolesRecord = Roles.objects.filter(userID =id)
                    serializer = SaveRolesSerializer(rolesRecord, many=True)
                    return Response({'message':'FETCH_SUCCESS','data':serializer.data}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
        