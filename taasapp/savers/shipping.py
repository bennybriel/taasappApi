from ..models import Shipping, Country,Courier
from ..serializers import SaveShippingSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveShippingView(APIView):
    serializer_class =SaveShippingSerializer
    @swagger_auto_schema(request_body=SaveShippingSerializer)
    def post(self, request):
         if request.method == 'POST':
         
            try:
                    serializer = SaveShippingSerializer(data=request.data)
                    
                    check = Shipping.objects.filter(courierID = request.data['courierID']).filter(location=request.data['location']).filter(userID = request.data['userID'])
                    #country_check = Country.objects.filter(id = request.data['countryID']).filter(userID = request.data['userID'])     
                    courier_check = Courier.objects.filter(id = request.data['courierID']).filter(userID = request.data['userID'])
                    # if not country_check:
                    #     return Response({"error": "Invalid Country", "statuscode":"404" ,"message":"NOT_FOUND" },status=status.HTTP_404_NOT_FOUND)           
                    if not courier_check:
                        return Response({"error": "Courier Not Found","statuscode":"404", "message":"NOT_FOUND" },status=status.HTTP_404_NOT_FOUND)           
                    if check:
                        shippingCount = Shipping.objects.filter(userID = request.data['userID']).count()
                        return Response({"statuscode":208, 'affectedRows':shippingCount, 'message':'ALREADY_EXIST', "error":" Record Already Exist"}, status=status.HTTP_208_ALREADY_REPORTED) 
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        
                        shippingCount = Shipping.objects.filter(userID = request.data['userID']).count()
                    
                        return Response({
                                        'userID':request.data['userID'],
                                        'affectedRows':shippingCount, 
                                        'expireDate':datetime.datetime.now(),
                                        'statuscode':200,
                                        'message':'SAVED_SUCCESS',
                                        }, status=status.HTTP_200_OK)
                    
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 