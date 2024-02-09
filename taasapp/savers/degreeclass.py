from ..models import Degreeclass
from ..serializers import SaveDegreeClassSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema

class SaveDegreeclassView(APIView):
    serializer_class =SaveDegreeClassSerializer
    @swagger_auto_schema(request_body=SaveDegreeClassSerializer)
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveDegreeClassSerializer(data=request.data)
        try:
            if serializer.is_valid():         
                name_check = Degreeclass.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
             
                if(name_check):
                    return Response({"error":"Name already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                serializer.save()
                degreeClassCount = Degreeclass.objects.filter(userID = request.data['userID']).count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':degreeClassCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request,id=None):
         if request.method == 'GET':
             DegreeclassRecord = Degreeclass.objects.filter(userID=id)
             return Response({'message':'SAVED_SUCCESS','data':list(DegreeclassRecord.values())}) 
             
           
        