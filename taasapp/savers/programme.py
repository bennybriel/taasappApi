from ..models import Department,Faculty, Programme
from ..serializers import SaveProgrammeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall
from  . . checkers import check_department_existence,check_programme_existence
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
           
    def get(self,request,id=None,dept=None):
         if request.method == 'GET':
             programmeRecord = Programme.objects.filter(userID=id).filter(departmentcode=dept)
             return Response({'message':'SAVED_SUCCESS','data':list(programmeRecord.values())}) 
     
class ListProgrammeView(APIView):
     #   @swagger_auto_schema(request_body=SaveDepartmentSerializer)
       def get(self,request,id=None):
         if request.method == 'GET':
              try:    
                  sql_query = """
                        SELECT pr.id, pr.name AS programme, dp.departmentcode, dp.name AS department, dp.departmentcode,dp.id as departmentid
                        FROM taasapp_programme pr
                        INNER JOIN taasapp_department dp ON pr.departmentcode = dp.departmentcode AND dp."userID" = pr."userID"
                        WHERE pr."userID" = %s
                        ORDER BY pr.name, dp.name;
                    """
                  with connection.cursor() as cursor:
                    cursor.execute(sql_query, [id])
                    if not cursor:
                        return Response({'message':'NOT_FOUND','data':cursor}) 
                        
                    results = cursor.fetchall()
                        # Process the results as needed
                    data = [{'id': row[0], 'programme': row[1],'programmecode':row[2],'department':row[3], 'departmentcode':row[4],'departmentid':row[5]} for row in results]
                    if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                    if not data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':400}) 
                    # departmentRecords = Department.objects.filter(userID=id)
                    # if not departmentRecords:
                    #        return Response({'message':'NOT_FOUND','data':list(departmentRecords.values())}) 
               
                    # return Response({'message':'SAVED_SUCCESS','data':list(departmentRecords.values())}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class ProgrammeUpdateView(APIView):
    serializer_class =SaveProgrammeSerializer
    @swagger_auto_schema(request_body=SaveProgrammeSerializer)
    def post(self, request):
         if request.method == 'POST':
                try:
                        departmentcode    = request.data['departmentcode']
                        name              = request.data['name']
                        facultycode       = request.data['facultycode']
                        programmecode     = request.data['programmecode']
                        userID            = request.data['userID']
                        id                = request.data['id']
                       
                        if not check_department_existence(request):
                              return Response({"error":"Department Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                        
                        if check_programme_existence(request):
                               return Response({"error": "Programme code already exists","statuscode": 208,"message": 'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED)
                               
                        prog = Programme.objects.get(id=id)
                        prog.name = name
                        prog.facultycode = facultycode
                        prog.departmentcode = departmentcode
                        prog.programmecode = programmecode
                        prog.save()
                        programmeCount =Programme.objects.filter(userID = userID).count()
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':programmeCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         
         return Response({'message':'SERVER_ERORR','error':'Request Method Not Allowed', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 


class DeleteProgrammeView(APIView):
    def delete(self, request, id, format=None):
        try: 
          
            instance = Programme.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            