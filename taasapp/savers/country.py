from ..models import Country
from ..serializers import SaveCountrySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema
from rest_framework_api_key.permissions import HasAPIKey
from ..authenticateHeader import authenticate_user

class SaveCountryView(APIView):
    serializer_class =SaveCountrySerializer
    @swagger_auto_schema(request_body=SaveCountrySerializer)
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveCountrySerializer(data=request.data)
        try:
            if serializer.is_valid():
          
                #check = Country.objects.filter(countryID = request.data['countryID'])
                name_check = Country.objects.filter(name = request.data['name'])
                
                if(name_check):
                    return Response({"error":"Name already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                        
                serializer.save()
                countryCount = Country.objects.count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':countryCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request):
         if request.method == 'GET':
             try:
                             
                    countryRecord = Country.objects.all()
                    serializer = SaveCountrySerializer(countryRecord, many=True)
                    return Response({'message':'FETCH_SUCCESS','data':serializer.data}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
        