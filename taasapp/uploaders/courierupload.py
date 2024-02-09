from .. serializers import CourierUploadSerializer
from ..models import Courier
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import pandas as pd  
from django.db import transaction
from django.db.models import Q
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class CourierFileUploaderView(APIView):
    serializer_class = CourierUploadSerializer
    @swagger_auto_schema(request_body=CourierUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =CourierUploadSerializer(data=request.data)
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
                new_file = Courier(
                            
                            name= row["name"],
                            address =row["address"],
                            email = row["email"],
                            phone = row["phone"],
                            userID= userID,
                            createdBy= createdBy,
                        )
                ck = Courier.objects.filter(name = row['name']).filter(userID = userID)
                ck_email = Courier.objects.filter(email = row['email']).filter(userID = userID)
                ck_phone = Courier.objects.filter(phone = row['phone']).filter(userID = userID)
                if not ck:
                    if not ck_email:     
                        if not ck_phone:
                            new_file.save()
                    
        
            recordCounter = Courier.objects.filter(userID = request.data['userID']).count()            
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter})
        except Exception as e:
               return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      
# class CourierFileUploaderView(APIView):
#      serializer_class = CourierUploadSerializer
#      @swagger_auto_schema(request_body=CourierUploadSerializer)
#      def post(self, request, *args, **kwargs):
#         serializer = CourierUploadSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         file = serializer.validated_data['file']
#         created_by = serializer.validated_data['createdBy']
#         user_id = serializer.validated_data['userID']
        
#         if not is_valid_csv(file):
#             return Response({"status": "error", "error": "Invalid or empty CSV file","message":"NOT_FILE"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             with transaction.atomic():
#                 reader = pd.read_csv(file)

#                 couriers_to_create = []
#                 for _, row in reader.iterrows():
#                     courier_data = {
#                         "name": row["name"],
#                         "address": row["address"],
#                         "email": row["email"],
#                         "phone": row["phone"],
#                         "userID": user_id,
#                         "createdBy": created_by,
#                     }
#                     couriers_to_create.append(Courier(**courier_data))

#                 # Use bulk_create for efficient batch insertion
#                 Courier.objects.bulk_create(couriers_to_create, ignore_conflicts=True)

#             record_counter = Courier.objects.filter(userID=user_id).count()
#             return Response({"status": "success", "message": "UPLOAD_SUCCESS", "affectedRows": record_counter})
#         except Exception as e:
#             return Response({'message': 'SERVER_ERROR', 'error': repr(e), 'expireDate': datetime.datetime.now(),
#                              'statuscode': '500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
