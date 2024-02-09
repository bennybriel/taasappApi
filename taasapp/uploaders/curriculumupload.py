from .. serializers import CurriculumUploadSerializer
from ..models import Courses, Curriculum, Level, Session, Semester,Department
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import pandas as pd  
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class CurriculumFileUploaderView(APIView):
    serializer_class = CurriculumUploadSerializer
    @swagger_auto_schema(request_body=CurriculumUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =CurriculumUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        createdBy = serializer.validated_data['createdBy']
        userID    = serializer.validated_data['userID']
        if not is_valid_csv(file):
            return Response({"message":"NOT_UPLOAD","error":"Only CSV files are allowed.","status":404},status=status.HTTP_400_BAD_REQUEST) 
        
        if not isfileuploadpermission(userID):
             return Response({"status": "404","message":"NOT_FOUND","error":"You are authorized to use this resources"}, status.HTTP_403_FORBIDDEN)

        k=0;
        try:
            
            reader = pd.read_csv(file)
            for _, row in reader.iterrows():
                k+=1
                check_level     = Level.objects.filter(name = row['level']).filter(userID = request.data['userID'])
                check_semester  = Semester.objects.filter(id = row['semester']).filter(userID = request.data['userID'])
                check_session   = Session.objects.filter(id = row['session']).filter(userID = request.data['userID'])
                check_dept      = Department.objects.filter(departmentcode =row['departmentcode']).filter(userID = request.data['userID'])
                check_course    = Courses.objects.filter(coursecode = row['coursecode']).filter(userID = request.data['userID'])

                new_file = Curriculum(
                                coursecode    = row["coursecode"],
                                courseunit    = row["courseunit"],
                                coursestatus  = row["coursestatus"],  
                                session       = row["session"], 
                                level         = row["level"],  
                                semester      = row["semester"],  
                                departmentcode= row["departmentcode"],                           
                                userID= userID,
                                createdBy= createdBy)
                
        
                ck = Curriculum.objects.filter(coursecode = row['coursecode']).filter(semester = row['semester']).filter(session = row['session']).filter(departmentcode = row['departmentcode']).filter(userID = userID)   
                if not ck and check_level and check_course and check_dept and check_semester and check_session: new_file.save()
                
                recordCounter = Curriculum.objects.filter(userID =userID).count()            
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter}, status.HTTP_201_CREATED)        
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
               