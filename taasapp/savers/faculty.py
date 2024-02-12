from ..models import Faculty
from ..serializers import SaveFacultySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema

class SaveFacultyView(APIView):
    serializer_class =SaveFacultySerializer
    @swagger_auto_schema(request_body=SaveFacultySerializer)
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveFacultySerializer(data=request.data)
        try:
            if serializer.is_valid():
                
                check = Faculty.objects.filter(facultycode = request.data['facultycode']).filter(userID = request.data['userID'])
                if(check):
                    return Response({"error":"Facultycode already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)

                name_check = Faculty.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
             
                if(name_check):
                    return Response({"error":"Name already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
               
                # if check:
                #      facultyCount = Faculty.objects.filter(userID = request.data['userID']).count()
                #      return Response({"statuscode":208, 'affectedRows':facultyCount,'message':'ALREADY_EXIST', "error":" FacultyID Supplied Already Exist"}, status=status.HTTP_208_ALREADY_REPORTED) 
                
                
                serializer.save()
                facultyCount = Faculty.objects.filter(userID = request.data['userID']).count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':facultyCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request,id=None):
         if request.method == 'GET':
             facultyRecord = Faculty.objects.filter(userID=id)
             return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(facultyRecord.values())}) 
             
           
class DeleteFacultyView(APIView):
    def delete(self, request, id, format=None):
        try: 
            print(id)          
            instance = Faculty.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            