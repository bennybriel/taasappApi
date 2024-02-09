from .. serializers import ShippingUploadSerializer
from ..models import Courier,Shipping,Country
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
import pandas as pd  
from .. fileformatchecker import is_valid_csv
from .. uploadpermission import isfileuploadpermission

class ShippingFileUploaderView(APIView):
    serializer_class = ShippingUploadSerializer
    @swagger_auto_schema(request_body=ShippingUploadSerializer)
    def post(self, request, *args, **kwargs):    
        serializer =ShippingUploadSerializer(data=request.data)
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
                country_check = Country.objects.filter(id = row['countryID']).filter(userID = userID)
                courier_check = Courier.objects.filter(id = row['courierID']).filter(userID = userID)
                new_file = Shipping(
                            
                            location= row["location"],
                            countryID =row["countryID"],
                            courierID = row["courierID"],
                            cost = row["cost"],
                            userID= userID,
                            createdBy= createdBy,
                        )
                ck = Shipping.objects.filter(courierID = row['courierID']).filter(userID = userID)
                if not ck and country_check and courier_check:
                    new_file.save()
                    
        
            recordCounter = Shipping.objects.filter(userID = request.data['userID']).count()            
            return Response({"status": "success","message":"UPLOAD_SUCCESS","affectedRows": recordCounter})
        
        except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
