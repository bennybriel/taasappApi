from ..models import Department,Faculty, Programme
from ..serializers import SaveProgrammeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema

class SaveProgrammeView(APIView):
    serializer_class =SaveProgrammeSerializer
    @swagger_auto_schema(request_body=SaveProgrammeSerializer)
    def post(self, request):
         
         if request.method == 'POST':      
            serializer = SaveProgrammeSerializer(data=request.data)
           
         try:  
               
                    check = Programme.objects.filter(name = request.data['programmecode']).filter(userID = request.data['userID'])
                    name_check = Programme.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
                    department_check =  Department.objects.filter(userID = request.data['userID'],departmentcode=request.data["departmentcode"])
                    faculty_check =  Faculty.objects.filter(userID = request.data['userID']).filter(facultycode=request.data["facultycode"])

                    if(check):
                         return Response({"error":"Programmecode already exists","statuscode":208, "message":"ALREADY_EXIST" },status=status.HTTP_208_ALREADY_REPORTED)
                    if not faculty_check:
                         return Response({"error":"Facultycode Not Exist","statuscode":404,"message":"NOT_FOUND" },status=status.HTTP_404_NOT_FOUND)
                    if not department_check:
                         return Response({"error":"Departmentcode Not Exist","statuscode":404,"message":"NOT_FOUND" },status=status.HTTP_404_NOT_FOUND)
                    if(name_check):
                         return Response({"error":"Programme already exists","statuscode":208, "message":"ALREADY_EXIST" },status=status.HTTP_208_ALREADY_REPORTED)
                    
                    if serializer.is_valid(raise_exception=True): 
                         serializer.save();
                       
                         programmeCount = Programme.objects.filter(userID = request.data['userID']).count()
                         
                    
                         return Response({
                                        'userID':request.data['userID'],
                                        'affectedRows':programmeCount, 
                                        'expireDate':datetime.datetime.now(),
                                        'message':'SAVED_SUCCESS',
                                        'statuscode':200,
                                        }, status=status.HTTP_200_OK)
                         
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         except Exception as e:
                        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                         #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
               


class SaveProgrammeViewAPI(APIView):
    serializer_class =SaveProgrammeSerializer
    @swagger_auto_schema(request_body=SaveProgrammeSerializer)
    def post(self, request):
         
         if request.method == 'POST':      
            serializer = SaveProgrammeSerializer(data=request.data)
           
         try:  
               
               
                    #check      = Programme.objects.filter(programmeID = request.data['programmeID']).filter(userID = request.data['userID'])
                    name_check =        Programme.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
                    department_check =  Department.objects.filter(userID = request.data['userID']).filter(id=request.data["departmentID"])
                    faculty_check =     Faculty.objects.filter(userID = request.data['userID']).filter(id=request.data["facultyID"])

                            
                    if not faculty_check:
                         return Response({"error":"FacultyID Not Exist","statuscode":404,"message":"NOT_FOUND" },status=status.HTTP_404_NOT_FOUND)
                    
                    if not department_check:
                         return Response({"error":"DepartmentID Not Exist","statuscode":404,"message":"NOT_FOUND" },status=status.HTTP_404_NOT_FOUND)
                    if(name_check):
                         return Response({"error":"Programme already exists","statuscode":208, "message":"ALREADY_EXIST" },status=status.HTTP_208_ALREADY_REPORTED)
                    
                    #check = checks(request.data['userID'], request.data['departmentID'])
                    
                    # if check:
                    #      programmeCount = Programme.objects.filter(userID = request.data['userID']).count()
                    #      return Response({"statuscode":208, 'affectedRows':programmeCount, "error":" ProgrammeID Supplied Already Exist","message":"ALREADY_EXIST"}, status=status.HTTP_208_ALREADY_REPORTED) 
                    if serializer.is_valid(raise_exception=True): 
                         # prog = Programme(name=request.data["name"])
                         # prog.userID = request.data["userID"]
                         # prog.createdBy = request.data["createdBy"]
                         # prog.departmentID=departments['id']
                         # prog.facultyID=facultys['id']
                         serializer.save();
                       
                         programmeCount = Programme.objects.filter(userID = request.data['userID']).count()
                         
                    
                         return Response({
                                        'userID':request.data['userID'],
                                        'affectedRows':programmeCount, 
                                        'expireDate':datetime.datetime.now(),
                                        'message':'SAVED_SUCCESS',
                                        'statuscode':200,
                                        }, status=status.HTTP_200_OK)
                         
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         except Exception as e:
                        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                         #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
           
    @staticmethod    
    def departmentCount(userID):
         departmentCount = Department.objects.filter(userID = request.data['userID']).count()
         return(departmentCount)
     
    @staticmethod
    def checks(userID, ID):
         ck = Department.objects.filter(departmentID = ID).filter(userID = userID)
         return(ck)
                    