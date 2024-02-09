from ..models import Semester,Session,SemesterResult,Department,StudentRecords,Level
from ..serializers import SaveSemesterResultSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveSemesterResultView(APIView):
    serializer_class =SaveSemesterResultSerializer
    @swagger_auto_schema(request_body=SaveSemesterResultSerializer)
    def post(self, request):
         if request.method == 'POST':
            try:
                serializer = SaveSemesterResultSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                   
                    level_check = Level.objects.filter(name = request.data['level']).filter(userID = request.data['userID'])
                    if not level_check:
                          return Response({"error":"Level Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)

                    session_check = Session.objects.filter(id = request.data['sessionID']).filter(userID = request.data['userID'])
                    if not session_check:
                          return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                      
                    semester_check = Semester.objects.filter(id = request.data['semesterID']).filter(userID = request.data['userID'])
                    if not semester_check:
                        return Response({"error":"Semester Not exists","statuscode":208, 'message':'NOT_FOUND' },status=status.HTTP_404_NOT_FOUND)
                  
                    check_dept = Department.objects.filter(departmentcode = request.data['departmentcode']).filter(userID = request.data['userID'])
                    if not check_dept:
                        return Response({"error":"Department Not exists","statuscode":404, 'message':'NOT_FOUND' },status=status.HTTP_404_NOT_FOUND)
            
                    matricno_check = StudentRecords.objects.filter(matricno = request.data['matricno'])             
                    if not matricno_check:
                         return Response({"statuscode":404, 'message':'NOT_FOUND', "error":"Matricno Not Exist"}, status=status.HTTP_404_NOT_FOUND) 

                    check = SemesterResult.objects.filter(matricno = request.data['matricno']).filter(level = request.data['level']).filter(sessionID = request.data['sessionID']).filter(semesterID = request.data['semesterID'])
                    if check:
                        return Response({"error":"Semester result already exists","statuscode":208, 'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)
             
                    serializer.save()
                    semesterResultCount = SemesterResult.objects.filter(userID = request.data['userID']).count()
                
                    return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':semesterResultCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            except Exception as e:
               return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def get(self,request,id=None):
        if request.method == 'GET':
            semesterResultRecords = SemesterResult.objects.filter(userID=id)
            return Response({'message':'SAVED_SUCCESS','data':list(semesterResultRecords.values())}) 
        
        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

        