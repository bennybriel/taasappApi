from ..models import State,Country
from ..serializers import SaveStateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema

class SaveStateView(APIView):
    serializer_class =SaveStateSerializer
    @swagger_auto_schema(request_body=SaveStateSerializer)
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveStateSerializer(data=request.data)
        try:
            
            
          
                countrys =  Country.objects.filter(userID = request.data['userID']).filter(name__contains=request.data["country"]).values("id").get()
                name_check = State.objects.filter(name = request.data['name'])
                
                if(name_check):
                    return Response({"error":"Name already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                # if check:
                #      stateCount = State.objects.filter(userID = request.data['userID']).count()
                #      return Response({"statuscode":208, 'affectedRows':stateCount,'message':'ALREADY_EXIST', "error":" StateID Supplied Already Exist"}, status=status.HTTP_208_ALREADY_REPORTED) 
                if serializer.is_valid(): 
                    state = State(userID = request.data['userID'])
                    state.name  = request.data['name']
                    state.createdBy = request.data['createdBy']
                    state.countryID = countrys['id']
                    
                    state.save()
                    stateCount = State.objects.count()
                
                    return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':stateCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'message':'SAVED_SUCCESS',
                                    'statuscode':200,
                                    }, status=status.HTTP_200_OK)
                return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request):
         if request.method == 'GET':
             stateRecord = State.objects.all()
             serializer = SaveCountrySerializer(stateRecord, many=True)
             return Response({'message':'SAVED_SUCCESS','data':serializer.data}) 
             
    def get(self,request, cid=None):
         if request.method == 'GET':
             stateRecord = State.objects.filter(countryID=cid)
             return Response({'message':'SAVED_SUCCESS','data':list(stateRecord.values())}) 
                    
        