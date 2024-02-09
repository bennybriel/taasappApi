from .. serializers import StudentRecordsUploadSerializer
from ..models import Faculty,Department,State,Country,StudentRecords, Degreeclass
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import io, csv, pandas as pd
from datetime import datetime
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class StudentRecordFileUploaderView(APIView):
    serializer_class = StudentRecordsUploadSerializer
    @swagger_auto_schema(request_body=StudentRecordsUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =StudentRecordsUploadSerializer(data=request.data)
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
                department_check =  Department.objects.filter(userID = request.data['userID']).filter(departmentcode=row["departmentcode"])
                faculty_check    =  Faculty.objects.filter(userID = request.data['userID']).filter(facultycode=row["facultycode"])
                country_check    =  Country.objects.filter(userID = request.data['userID']).filter(id=row["countryID"])
                state_check      =  State.objects.filter(userID = request.data['userID']).filter(id=row["stateID"])
                degree_check      =  Degreeclass.objects.filter(userID = request.data['userID']).filter(id=row["degreeclassID"])
                new_file = StudentRecords(
                                matricno    = row["matricno"],
                                surname     = row["surname"],
                                firstname   = row["firstname"],
                                othername   = row["othername"],
                                dob         = row["dob"],
                                gender      = row["gender"],
                                phone       = row["phone"],
                                address     = row["address"],
                                email       = row["email"],
                                cgpa        = row["cgpa"],
                                stateID       = row["stateID"],
                                facultycode         = row["facultycode"],
                                departmentcode      = row["departmentcode"],
                                graduationyear      = row["graduationyear"],
                                countryID         = row["countryID"],
                                degreeofclass       = row["degreeclassID"],
                                entryyear           = row["entryyear"],
                                userID      = userID,
                                createdBy   = createdBy,
                            )
                ck = StudentRecords.objects.filter(matricno = row['matricno']).filter(userID = userID)
                if not ck and department_check and faculty_check and state_check and degree_check and state_check and country_check: new_file.save()
       
            recordCounter = StudentRecords.objects.filter(userID = request.data['userID']).count()            
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter})
        except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
