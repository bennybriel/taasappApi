from ..models import Grade
from ..serializers import SaveGradeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveGradeView(APIView):
    serializer_class =SaveGradeSerializer
    @swagger_auto_schema(request_body=SaveGradeSerializer)
    def post(self, request):
         if request.method == 'POST':
              try:
                      
                   serializer = SaveGradeSerializer(data=request.data)
                   print(request.data)
                   if serializer.is_valid():
                         minscore, maxscore = request.data['minscore'], request.data['maxscore']
                         if minscore > maxscore:
                              return Response({"statuscode":406, 'message':'ALREADY_EXIST', "error": "Min score cannot be greater than max score"},status=status.HTTP_406_NOT_ACCEPTABLE)
                        
                         check = Grade.objects.filter(grade = request.data['grade'],userID = request.data['userID'])                    
                         if check:
                              gradeCount = Grade.objects.filter(userID = request.data['userID']).count()
                              return Response({"statuscode":208,  'message':'ALREADY_EXIST', 'affectedRows':gradeCount, "error":" Grade Already Exist"}, status=status.HTTP_208_ALREADY_REPORTED) 
                         
                         serializer.save()
                         gradeCount = Grade.objects.filter(userID = request.data['userID']).count()
               
                         return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':gradeCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'statuscode':200,
                                 'message':'SAVED_SUCCESS',
                                }, status=status.HTTP_200_OK)
                         
                   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
              except Exception as e:
               return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


    def get(self,request,id=None):  
            try:
                if request.method == 'GET':
                    gradeRecords = Grade.objects.filter(userID=id)
                    return Response({'message':'SAVED_SUCCESS','data':list(gradeRecords.values())}) 
            
            except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
            
        