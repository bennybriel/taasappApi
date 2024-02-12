from ..models import Department,Faculty
from ..serializers import SaveDepartmentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall
from  . . checkers import check_department_existence,check_faculty_existence
class SaveDepartmentView(APIView):
    serializer_class =SaveDepartmentSerializer
    @swagger_auto_schema(request_body=SaveDepartmentSerializer)
    def post(self, request):
         if request.method == 'POST':
                   serializer = SaveDepartmentSerializer(data=request.data)
                   
                   try:  
                         if serializer.is_valid(raise_exception=True):     
                              if not check_faculty_existence(request):
                                   return Response({"error":"Faculty Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                              if check_department_existence(request):
                                    return Response({"error": "Department code already exists","statuscode": 208,"message": 'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED)
                              
                              name_check = Department.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])                   
                              if(name_check):
                                   return Response({"error":"Name already exists","statuscode":208,  'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED) 
                              departmentCount = Department.objects.filter(userID = request.data['userID']).count()
                              serializer.save()     
                                  
                              return Response({
                                                       'userID':request.data['userID'],
                                                       'affectedRows':departmentCount, 
                                                       'expireDate':datetime.datetime.now(),
                                                       'statuscode':200,
                                                       'message':'SAVED_SUCCESS',
                                                       }, status=status.HTTP_200_OK)
                                   
                         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
                     
                   except Exception as e:
                        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def get(self,request,id=None,fac=None):
         if request.method == 'GET':
             departmentRecord = Department.objects.filter(userID=id).filter(facultycode=fac)
             return Response({'message':'SAVED_SUCCESS','data':list(departmentRecord.values())}) 
     
class SaveDepartmentViewAPI(APIView):
    serializer_class =SaveDepartmentSerializer
    @swagger_auto_schema(request_body=SaveDepartmentSerializer)
    def post(self, request):
         if request.method == 'POST':
                   serializer = SaveDepartmentSerializer(data=request.data)
                   
                   try:        
                              facultys =  Faculty.objects.filter(userID =  request.data['userID']).filter(name__contains= request.data["faculty"]).values("id").get()                                             
                              if not facultys:
                                   return Response({"error":"Faculty Not Exist","statuscode":404,"message":"NOT_FOUND"  },status=status.HTTP_404_NOT_FOUND)
                              name_check = Department.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
                              faculty_check =Faculty.objects.filter(id =facultys['id']).filter(userID = request.data['userID'])
                              if not faculty_check:
                                   return Response({"error":"Facultycode Not Exist","statuscode":404,"message":"NOT_FOUND"  },status=status.HTTP_404_NOT_FOUND)
                              
                              if(name_check):
                                   return Response({"error":"Name already exists","statuscode":208,  'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)
                              
                                 
                              
                              
                              if serializer.is_valid(raise_exception=True): 
                                   dept = Department(name=request.data['name'])
                                   dept.facultycode = facultys["id"]
                                   dept.faculty = request.data['faculty']
                                   dept.userID =     request.data['userID']
                                   dept.createdBy =  request.data['createdBy']
                                   dept.save()
                                   
                                   departmentCount = Department.objects.filter(userID = request.data['userID']).count()
                                        
                              
                                   return Response({
                                                       'userID':request.data['userID'],
                                                       'affectedRows':departmentCount, 
                                                       'expireDate':datetime.datetime.now(),
                                                       'statuscode':200,
                                                       'message':'SAVED_SUCCESS',
                                                       }, status=status.HTTP_200_OK)
                                   
                              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
                     
                   except Exception as e:
                        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                                             
    def get(self,request,id=None,fac=None):
         if request.method == 'GET':
           
             departmentRecord = Department.objects.filter(userID=id).filter(facultycode=fac)
             return Response({'message':'SAVED_SUCCESS','data':list(departmentRecord.values())}) 


class ListDepartmentView(APIView):
     #   @swagger_auto_schema(request_body=SaveDepartmentSerializer)
       def get(self,request,id=None):
         if request.method == 'GET':
              try:    
                  sql_query = """
                        SELECT dp.id, dp.name AS department, dp.departmentcode, fa.name AS faculty, dp.facultycode,fa.id as facultyid
                        FROM taasapp_department dp
                        INNER JOIN taasapp_faculty fa ON fa.facultycode = dp.facultycode AND dp."userID" = fa."userID"
                        WHERE dp."userID" = %s
                        ORDER BY dp.name, fa.name;
                    """
                  with connection.cursor() as cursor:
                    cursor.execute(sql_query, [id])
                    if not cursor:
                        return Response({'message':'NOT_FOUND','data':cursor}) 
                        
                    results = cursor.fetchall()
                        # Process the results as needed
                    data = [{'id': row[0], 'department': row[1],'departmentcode':row[2],'faculty':row[3], 'facultycode':row[4],'facultyid':row[5]} for row in results]
                    if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                    if not data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':400}) 
                    # departmentRecords = Department.objects.filter(userID=id)
                    # if not departmentRecords:
                    #        return Response({'message':'NOT_FOUND','data':list(departmentRecords.values())}) 
               
                    # return Response({'message':'SAVED_SUCCESS','data':list(departmentRecords.values())}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class DepartmentUpdateView(APIView):
    serializer_class =SaveDepartmentSerializer
    @swagger_auto_schema(request_body=SaveDepartmentSerializer)
    def post(self, request):
         if request.method == 'POST':
                try:
                        departmentcode = request.data['departmentcode']
                        name           = request.data['department']
                        facultycode     = request.data['facultycode']
                        userID         = request.data['userID']
                        id             = request.data['id']
                     
                     
                        if not check_faculty_existence(request):
                              return Response({"error":"Faculty Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                        if check_department_existence(request):
                               return Response({"error": "Department code already exists","statuscode": 208,"message": 'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED)
                               
                        dept = Department.objects.get(id=id)
                        dept.name = name
                        dept.departmentcode = departmentcode
                        dept.facultycode = facultycode
                        dept.save()
                        departmentCount = Department.objects.filter(userID = userID).count()
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':departmentCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         
         return Response({'message':'SERVER_ERORR','error':'Request Method Not Allowed', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 


class DeleteDepartmentView(APIView):
    def delete(self, request, id, format=None):
        try: 
                 
            instance = Department.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            