from ..models import SchoolSettings, State, Country
from ..serializers import SaveSchoolSettingsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class SaveSchoolSettingView(APIView):
   serializer_class =SaveSchoolSettingsSerializer
   parser_classes = (MultiPartParser, FormParser)
   @swagger_auto_schema(request_body=SaveSchoolSettingsSerializer)
   def post(self, request):
         if request.method == 'POST':
            try:
                  serializer = SaveSchoolSettingsSerializer(data=request.data)
               
                  check = SchoolSettings.objects.filter(userID=request.data['userID'])
                  if check:
                     return Response({"statuscode":208,  "error":" School Information Already Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 
               
                  if serializer.is_valid(raise_exception=True):            
                     serializer.save()
                     return Response({
                                       'userID':request.data['userID'],
                                       'expireDate':datetime.datetime.now(),
                                       'message':'SAVED_SUCCESS',
                                       'statuscode':200,
                                       }, status=status.HTTP_200_OK)
                  #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                  return Response({'message':'SERVER_ERORR','error':serializer.errors, 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 
            except Exception as e:
               return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
