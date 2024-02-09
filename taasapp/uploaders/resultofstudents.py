from ..models import ResultOfStudents,Department,Session,Semester, Grade, Level,StudentRecords
from ..serializers import StudentResultsUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
import pandas as pd  
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class StudentResultsFileUploaderView(APIView):
    serializer_class = StudentResultsUploadSerializer
    @swagger_auto_schema(request_body=StudentResultsUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =StudentResultsUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
       
        file = serializer.validated_data['file']
        createdBy = serializer.validated_data['createdBy']
        userID    = serializer.validated_data['userID']
        if not is_valid_csv(file):
            return Response({"message":"NOT_UPLOAD","error":"Only CSV files are allowed.","status":404},status=status.HTTP_400_BAD_REQUEST) 
        
        if not isfileuploadpermission(userID):
             return Response({"status": "404","message":"NOT_FOUND","error":"You are authorized to use this resources"}, status.HTTP_403_FORBIDDEN)

        try:
            
            reader = pd.read_csv(file)
            for _, row in reader.iterrows():
                session_check    =  Session.objects.filter(userID = request.data['userID']).filter(id=row["sessionID"])
                level_check      =  Level.objects.filter(userID = request.data['userID']).filter(name=row["level"])
                semester_check   =  Semester.objects.filter(userID = request.data['userID']).filter(id=row["semesterID"])
                department_check =  Department.objects.filter(userID = request.data['userID']).filter(departmentcode=row["departmentcode"])
                grade_check      =  Grade.objects.filter(userID = request.data['userID']).filter(grade=row["grade"])
                point_check      =  Grade.objects.filter(userID = request.data['userID']).filter(point=row["point"])
                matricno_check   =  StudentRecords.objects.filter(userID = request.data['userID']).filter(matricno=row["matricno"])      
                new_file = ResultOfStudents(
                                matricno       = row["matricno"],
                                departmentcode = row["departmentcode"],
                                semesterID     = row['semesterID'],
                                levelID        = row["level"],
                                score          = row["score"],
                                coursecode     = row["coursecode"],
                                point          = row["point"],
                                grade          = row["grade"],
                                sessionID      = row['sessionID'],
                                userID         = userID,
                                createdBy      = createdBy,
                            )
                ck = ResultOfStudents.objects.filter(matricno = row['matricno']).filter(userID = userID).filter(sessionID=row['sessionID']).filter(semesterID = row["semesterID"]).filter(levelID = row["level"]).filter(coursecode = row["coursecode"])
                
                # and level_check and department_check and semester_check and session_check and point_check and grade_check  
                if not ck and  matricno_check and level_check and department_check and semester_check and session_check and point_check and grade_check : new_file.save()
                
            recordCounter = ResultOfStudents.objects.filter(userID = request.data['userID']).count()  
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
             
                 
