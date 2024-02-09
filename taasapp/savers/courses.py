from ..models import Courses
from ..serializers import SaveCoursesSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveCoursesView(APIView):
    serializer_class =SaveCoursesSerializer
    @swagger_auto_schema(request_body=SaveCoursesSerializer)
    def post(self, request):
        if request.method == 'POST':
            try:
                 serializer = SaveCoursesSerializer(data=request.data)
                 if serializer.is_valid():
                   
                    check      = Courses.objects.filter(coursecode = request.data['coursecode']).filter(userID = request.data['userID'])
                              
                    if check:
                        courseCount = Courses.objects.filter(userID = request.data['userID']).count()    
                        # courseCount = Courses.objects.filter(userID = request.data['userID']).count()
                        return Response({"statuscode":208, 'affectedRows':courseCount, "error":" Coursecode Supplied Already Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 
                        
                    
                    serializer.save()
                    courseCount = Courses.objects.filter(userID = request.data['userID']).count()    
                    return Response({
                                            'userID':request.data['userID'],
                                            'affectedRows':courseCount, 
                                            'expireDate':datetime.datetime.now(),
                                            'statuscode':200,
                                            'message':'SAVED_SUCCESS',
                                            }, status=status.HTTP_200_OK)
                            
                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                
            except Exception as e:
                print(e)
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    def get(self,request,id=None):
         if request.method == 'GET':
              try:    
                    courseRecords = Courses.objects.filter(userID=id)
                    if not courseRecords:
                           return Response({'message':'NOT_FOUND','data':list(courseRecords.values())}) 
               
                    return Response({'message':'SAVED_SUCCESS','data':list(courseRecords.values())}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
            
