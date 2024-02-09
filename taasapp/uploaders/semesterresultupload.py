from ..models import Department,Session,Semester, Level,SemesterResult,StudentRecords
from ..serializers import SemesterResultsUploadSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
import pandas as pd  
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class SemesterResultsFileUploaderView(APIView):
    serializer_class = SemesterResultsUploadSerializer
    @swagger_auto_schema(request_body=SemesterResultsUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =SemesterResultsUploadSerializer(data=request.data)
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
            print(reader)
            for _, row in reader.iterrows():
                session_check    =  Session.objects.filter(userID = request.data['userID']).filter(id=row["sessionID"])
                level_check      =  Level.objects.filter(userID = request.data['userID']).filter(name=row["level"])
                semester_check   =  Semester.objects.filter(userID = request.data['userID']).filter(id=row["semesterID"])
                department_check =  Department.objects.filter(userID = request.data['userID']).filter(departmentcode=row["departmentcode"])
                matricno_check   =  StudentRecords.objects.filter(userID = request.data['userID']).filter(matricno=row["matricno"])      
               
                new_file = SemesterResult(
                                matricno       = row["matricno"],
                                departmentcode = row["departmentcode"],
                                semesterID     = row['semesterID'],
                                level        = row["level"],
                                gpa            = row["gpa"],
                                cgpa           = row["cgpa"],
                                sessionID      = row['sessionID'],
                                userID         = userID,
                                createdBy      = createdBy,
                            )
                ck = SemesterResult.objects.filter(matricno = row['matricno']).filter(userID = userID).filter(sessionID=row['sessionID']).filter(semesterID = row["semesterID"]).filter(level = row["level"])
                
                # and level_check and department_check and semester_check and session_check and point_check and grade_check  
                if not ck and  matricno_check and level_check and department_check and semester_check and session_check: new_file.save()
                
            recordCounter = SemesterResult.objects.filter(userID = request.data['userID']).count()  
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
             
                 
