from .. serializers import GradeUploadSerializer
from ..models import Grade
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import io, csv, pandas as pd
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission


class GradeFileUploaderView(APIView):
    serializer_class = GradeUploadSerializer
    @swagger_auto_schema(request_body=GradeUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =GradeUploadSerializer(data=request.data)
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
                new_file = Grade(
                            
                            grade= row["grade"],
                            minscore =row["minscore"],
                            maxscore = row["maxscore"],
                            point = row["point"],
                            userID= userID,
                            createdBy= createdBy,
                        )
                ck = Grade.objects.filter(grade = row['grade']).filter(userID = userID)
                if not ck : new_file.save()
                    
        
            recordCounter = Grade.objects.filter(userID = request.data['userID']).count()            
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter})
        except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
            