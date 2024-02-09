
from .. serializers import SessionUploadSerializer
from ..models import Session
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import  pandas as pd   
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class SessionFileUploaderView(APIView):
    serializer_class = SessionUploadSerializer
    @swagger_auto_schema(request_body=SessionUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =SessionUploadSerializer(data=request.data)
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
                new_file = Session(
                           
                            name= row["name"],
                            userID= userID,
                            createdBy= createdBy,
                        )
                ck = Session.objects.filter(name = row['name']).filter(userID = userID)
                if not ck: new_file.save()
                    
        
            recordCounter = Session.objects.filter(userID = request.data['userID']).count()            
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter})
        except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
