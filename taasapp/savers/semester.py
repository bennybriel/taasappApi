from ..models import Semester,Session
from ..serializers import SaveSemesterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveSemesterView(APIView):
    serializer_class =SaveSemesterSerializer
    @swagger_auto_schema(request_body=SaveSemesterSerializer)
    def post(self, request):
         if request.method == 'POST':
            try:
                serializer = SaveSemesterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                   
                    check = Session.objects.filter(id = request.data['sessionID']).filter(userID = request.data['userID'])
                    if not check:
                          return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                      
                    name_check = Semester.objects.filter(name = request.data['name'],  userID = request.data['userID'], sessionID = request.data['sessionID'] )
                    
                    if(name_check):
                        return Response({"error":"Semester already exists for selected session","statuscode":208, 'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)
                
                                 
                    serializer.save()
                    semesterCount = Semester.objects.filter(userID = request.data['userID']).count()
                
                    return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':semesterCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            except Exception as e:
               return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def get(self,request,session=None,id=None):
        if request.method == 'GET':
            semesterRecords = Semester.objects.filter(sessionID=session,userID=id)
            return Response({'message':'SAVED_SUCCESS','data':list(semesterRecords.values())}) 
        
        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

        