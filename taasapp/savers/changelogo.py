from ..models import SchoolSettings
from ..serializers import SaveSchoolSettingsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from drf_yasg.utils import swagger_auto_schema
class SaveChangeLogoView(APIView):
    serializer_class =SaveSchoolSettingsSerializer
    @swagger_auto_schema(request_body=SaveSchoolSettingsSerializer)
    def post(self, request):
        if request.method == 'POST':
            
            try:
                check  = SchoolSettings.objects.filter(userID =request.data["userID"])
                if not check:
                    return Response({"error":"Sorry User Not Authorized","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
           
                school = SchoolSettings.objects.get(userID=request.data["userID"])
                school.userID = request.data["userID"]
                school.save()        
                if school:
                    
                    return Response({
                                 'userID':request.data['userID'],
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
                return Response({"error":"Logo Not Uploaded","statuscode":303, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
def logo_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "%s.%s"% (instance.userID, extension)
    return new_filename

        