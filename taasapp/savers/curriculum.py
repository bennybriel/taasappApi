from ..models import Curriculum, Department,Session, Semester, Level, Session,Courses
from ..serializers import SaveCurriculumSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall
class SaveCurriculumView(APIView):
    serializer_class =SaveCurriculumSerializer
    @swagger_auto_schema(request_body=SaveCurriculumSerializer)
    def post(self, request):
        if request.method == 'POST':
            try:
                 serializer = SaveCurriculumSerializer(data=request.data)
                 if serializer.is_valid():
                
                    check_level     = Level.objects.filter(name = request.data['level'],sessionID = request.data['session'],userID = request.data['userID'])
                    check_semester  = Semester.objects.filter(id = request.data['semester'],sessionID = request.data['session'], userID = request.data['userID'])
                    check_session   = Session.objects.filter(id = request.data['session'], userID = request.data['userID'])
                    check_dept      = Department.objects.filter(departmentcode = request.data['departmentcode']).filter(userID = request.data['userID'])
                    check_course    = Courses.objects.filter(coursecode = request.data['coursecode']).filter(userID = request.data['userID'])

                    if not check_dept:
                        return Response({"statuscode":404, "error":" Departmentcode Not Exist",  'message':'NOT_FOUND'}, status=status.HTTP_208_ALREADY_REPORTED) 
                    if not check_level:
                        return Response({"statuscode":404, "error":" Level Not Exist",  'message':'NOT_FOUND'}, status=status.HTTP_208_ALREADY_REPORTED) 
                    if not check_semester:
                        return Response({"statuscode":404, "error":" Semester Not Exist",  'message':'NOT_FOUND'}, status=status.HTTP_208_ALREADY_REPORTED) 
                    if not check_session:
                        return Response({"statuscode":404, "error":" Session Not Exist",  'message':'NOT_FOUND'}, status=status.HTTP_208_ALREADY_REPORTED) 
                    if not check_course:
                        return Response({"statuscode":404, "error":" Coursecode Not Exist",  'message':'NOT_FOUND'}, status=status.HTTP_208_ALREADY_REPORTED) 

                    check = Curriculum.objects.filter(coursecode = request.data['coursecode'],
                                                      semester   = request.data['semester'],
                                                      session    = request.data['session'],  
                                                      level      = request.data['level'],
                                                      departmentcode = request.data['departmentcode'],
                                                      userID = request.data['userID'])
                              
                    if check:
                        return Response({"statuscode":208, "error":" Coursecode Supplied Already Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 
                        
                    serializer.save()
                    curriculumCount = Curriculum.objects.filter(userID = request.data['userID']).count()
           
                    return Response({
                                            'userID':request.data['userID'],
                                            'affectedRows':curriculumCount, 
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
                    curriculumRecords = Curriculum.objects.filter(userID=id)
                    if not curriculumRecords:
                           return Response({'message':'NOT_FOUND','data':list(curriculumRecords.values())}) 
               
                    return Response({'message':'SAVED_SUCCESS','data':list(curriculumRecords.values())}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
 
class GetStudentCoursesView(APIView):
       def post(self,request):
         if request.method == 'POST':
           
                departmentcode= request.data['departmentcode']
                session= request.data['session']
                semester= request.data['semester']
                try:
                    sql_query = """
                    SELECT  coursecode,level,semester,session
                    FROM taasapp_curriculum
                    WHERE departmentcode =%s AND semester = %s AND session = %s;
                    """
                    with connection.cursor() as cursor:
                      cursor.execute(sql_query, [departmentcode, semester, session])
                      if not cursor:
                          return Response({'message':'NOT_FOUND','data':cursor}) 
                      
                      results = cursor.fetchall()
                     
                      # Process the results as needed
                      data = [{'coursecode': row[0], 'level': row[1],'semester': row[2],'session': row[3]} for row in results]
                      return Response(data)
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
          
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
