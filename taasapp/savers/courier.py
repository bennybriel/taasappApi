from ..models import Courier
from ..serializers import SaveCourierSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveCourierView(APIView):
    serializer_class =SaveCourierSerializer
    @swagger_auto_schema(request_body=SaveCourierSerializer)
    def post(self, request):
         if request.method == 'POST':
            serializer = SaveCourierSerializer(data=request.data)
            
            
            try:
                if serializer.is_valid():
                    check = Courier.objects.filter(email = request.data['email']).filter(userID = request.data['userID'])
                    phone_check = Courier.objects.filter(phone = request.data['phone']).filter(userID = request.data['userID'])
                    name_check = Courier.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
                    
                    if(name_check):
                        return Response({"error":"Name already exists","statuscode":208,  'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)
                
                    if(phone_check):
                        return Response({"error":"Phone already exists","statuscode":208,  'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)

                    if check:
                        courierCount = Courier.objects.filter(userID = request.data['userID']).count()
                        return Response({"statuscode":208, 'affectedRows':courierCount,  'message':'ALREADY_EXIST', "error":" Email Supplied Already Exist"}, status=status.HTTP_208_ALREADY_REPORTED) 
                    
                    serializer.save()
                    courierCount = Courier.objects.filter(userID = request.data['userID']).count()
                
                    return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':courierCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'message':'SAVED_SUCCESS',
                                    'statuscode':200,
                                    }, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def get(self,request,id=None):
        if request.method == 'GET':
            courierRecord = Courier.objects.filter(userID=id)
            return Response({'message':'SAVED_SUCCESS','data':list(courierRecord.values())}) 
                
