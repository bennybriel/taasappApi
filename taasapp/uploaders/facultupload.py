from .. serializers import FacultyUploadSerializer
from ..models import Faculty,Users
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import io, csv, pandas as pd
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission
class FacultyFileUploaderView(APIView):
    serializer_class = FacultyUploadSerializer
    @swagger_auto_schema(request_body=FacultyUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =FacultyUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        createdBy = serializer.validated_data['createdBy']
        userID    = serializer.validated_data['userID']
        
        if not is_valid_csv(file):
            return Response({"message":"NOT_UPLOAD","error":"Only CSV files are allowed.","status":404},status=status.HTTP_400_BAD_REQUEST) 
        
        if not isfileuploadpermission(userID):
             return Response({"status": "404","message":"NOT_FOUND","error":"You are authorized to use this resources"}, status.HTTP_403_FORBIDDEN)
            
        reader = pd.read_csv(file)
        try:
            for _, row in reader.iterrows():
                
                new_file = Faculty(
                        name= row["name"],
                        facultycode= row["facultycode"],
                        userID= userID,
                        createdBy= createdBy,
                        )
                ck = Faculty.objects.filter(facultycode = row['facultycode']).filter(userID = userID)
                if not ck: new_file.save()
            recordCounter = Faculty.objects.filter(userID = request.data['userID']).count()         
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter}, status.HTTP_201_CREATED)    
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  