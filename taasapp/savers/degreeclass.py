from ..models import Degreeclass
from ..serializers import SaveDegreeClassSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema
from ..checkers import check_session_existence
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
             return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(DegreeclassRecord.values())}) 
             

class DegreeUpdateView(APIView):
    serializer_class =SaveDegreeClassSerializer
    @swagger_auto_schema(request_body=SaveDegreeClassSerializer)
    def post(self, request):
         if request.method == 'POST':
                try:
                    
                        name     = request.data['name']
                        userID   = request.data['userID']
                        id       = request.data['id']
                        check = Degreeclass.objects.filter(userID =userID, name=name)
                        if(check):
                             return Response({"error": "Degree Class already exists","statuscode": 208,"message": 'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED)

                        degree = Degreeclass.objects.get(id=id)
                        degree.name = name
                        degree.userID = userID
                        degree.save()
                        degreeCount = Degreeclass.objects.filter(userID = request.data['userID']).count()
                    
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':degreeCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         
         return Response({'message':'SERVER_ERORR','error':'Request Method Not Allowed', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 

class DeleteDegreeView(APIView):
    def delete(self, request, id, format=None):
        try:  
            instance = Degreeclass.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                  