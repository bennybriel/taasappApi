from ..models import StudentRecords,Department, Faculty, State,Country,Degreeclass,Graduationyear,Curriculum
from ..serializers import SaveStudentRecordsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall

class SaveStudentRecordsView(APIView):
    serializer_class =SaveStudentRecordsSerializer
    @swagger_auto_schema(request_body=SaveStudentRecordsSerializer)
    def post(self, request):
         if request.method == 'POST':
               
                try:
                     serializer = SaveStudentRecordsSerializer(data=request.data)  
                     if serializer.is_valid(): 
                              
                        check = StudentRecords.objects.filter(matricno = request.data['matricno'], userID = request.data['userID'])
                        check_email = StudentRecords.objects.filter(email = request.data['email']).filter(userID = request.data['userID'])
                        check_phone = StudentRecords.objects.filter(phone = request.data['phone']).filter(userID = request.data['userID'])
                        check_faculty = Faculty.objects.filter(facultycode = request.data['facultycode']).filter(userID = request.data['userID'])
                        check_dept = Department.objects.filter(departmentcode = request.data['departmentcode']).filter(userID = request.data['userID'])
                        check_state = State.objects.filter(id = request.data['stateID'])
                        check_degree = Degreeclass.objects.filter(id = request.data['degreeofclass']).filter(userID = request.data['userID'])
                        check_graduation = Graduationyear.objects.filter(year = request.data['graduationyear']).filter(userID = request.data['userID'])
                        check_country = Country.objects.filter(id = request.data['countryID'])
                        if check:
                              return Response({"statuscode":208, "error":" Student Matricno Already Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 
      
                        if check_email:
                              return Response({"statuscode":208, "error":" Email Already Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 
                              
                        if check_phone:
                              return Response({"statuscode":208, "error":" Phone Number Already Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 

                              
                        if not check_faculty:
                              return Response({"statuscode":404, "error":" Facultycode Not Exist",  'message':'NOT_FOUND'}, status=status.HTTP_208_ALREADY_REPORTED) 
                              
                        if not check_dept:
                              return Response({"statuscode":404, "error":" Departmentcode Not Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 

                        if not check_state:
                              return Response({"statuscode":404, "error":" State ID Not Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 

                        if not check_degree:
                              return Response({"statuscode":404, "error":" Degree Class Not Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 

                        if not check_graduation:
                              return Response({"statuscode":404, "error":" Year of Graduation Not Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 

                        if not check_country:
                              return Response({"statuscode":404, "error":" Country ID Not Exist",  'message':'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED) 

                        serializer.save()
                        studentCount = StudentRecords.objects.filter(userID = request.data['userID']).count()
                                    
                              
                        return Response({
                                                'userID':request.data['userID'],
                                                'affectedRows':studentCount, 
                                                'expireDate':datetime.datetime.now(),
                                                'message':'SAVED_SUCCESS',
                                                'statuscode':200,
                                                }, status=status.HTTP_200_OK)
                        
                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                except Exception as e:
                  return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
class GetStudentInformationLists(APIView):
       serializer_class =SaveStudentRecordsSerializer
       def post(self,request):
         if request.method == 'POST':

             try:
                  userID   = request.data['userID']
                  matricno = request.data['matricno'] 
                  level    = request.data['level']    
                  semester = request.data['semester']   
                  session  = request.data['session']        
                      
                  studentrecords = StudentRecords.objects.filter(userID= userID, matricno = matricno).first();  
                  if not studentrecords:
                        return Response({'message':'NOT_FOUND', 'statuscode':"1"})                  
                  if studentrecords:
                        departmentcode = studentrecords.departmentcode
                 
                  
                  #courses = Curriculum.objects.filter(userID = userID).filter(level= level).filter(semester=semester).filter(session=session).filter(departmentcode=departmentcode).get()
                  courselist = Curriculum.objects.filter(
                                                            userID=userID,
                                                            level=level,
                                                            semester=semester,
                                                            session=session,
                                                            departmentcode=departmentcode
                                                      ).all()

                 
                  if courselist: return Response({'message':'SAVED_SUCCESS','statuscode':0,'data':list(courselist.values())}) 
                  if not courselist: return Response({'message':'NOT_FOUND','error':"No Record Found For Selected Options",'data':0, 'statuscode':"1"}) 
                  
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
      


     
