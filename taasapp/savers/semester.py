from ..models import Semester,Session
from ..serializers import SaveSemesterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall

class SaveSemesterView(APIView):
    serializer_class =SaveSemesterSerializer
    @swagger_auto_schema(request_body=SaveSemesterSerializer)
    def post(self, request):
         if request.method == 'POST':
            try:
                serializer = SaveSemesterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                   
                    check = Session.objects.filter(id = request.data['sessionID']).filter(userID = request.data['userID'])
                    if not check:
                          return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                      
                    name_check = Semester.objects.filter(name = request.data['name'],  userID = request.data['userID'], sessionID = request.data['sessionID'] )
                    
                    if(name_check):
                        return Response({"error":"Semester already exists for selected session","statuscode":208, 'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)
                
                                 
                    serializer.save()
                    semesterCount = Semester.objects.filter(userID = request.data['userID']).count()
                
                    return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':semesterCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            except Exception as e:
               return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def get(self,request,session=None,id=None):
        if request.method == 'GET':
            semesterRecords = Semester.objects.filter(sessionID=session,userID=id)
            return Response({'message':'SAVED_SUCCESS','data':list(semesterRecords.values())}) 
        
        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


 
class ListSemesterView(APIView):
     #   @swagger_auto_schema(request_body=SaveDepartmentSerializer)
       def get(self,request,id=None):
         if request.method == 'GET':
              try:    
                sql_query = """
                        SELECT sm.id, sm.name AS semester, se.name AS session, se.id
                        FROM taasapp_semester sm
                        INNER JOIN taasapp_session se ON sm."sessionID" = se."id"
                        WHERE sm."userID" = %s
                        ORDER BY sm.name, se.name;
                    """
                with connection.cursor() as cursor:
                    cursor.execute(sql_query, [id])
                    if not cursor:
                        return Response({'message':'NOT_FOUND','data':cursor}) 
                        
                    results = cursor.fetchall()
                        # Process the results as needed
                    data = [{'id': row[0], 'semester': row[1],'session':row[2],'sessionID':row[3]} for row in results]
                    if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                    if not data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':400}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class SemesterUpdateView(APIView):
    serializer_class =SaveSemesterSerializer
    @swagger_auto_schema(request_body=SaveSemesterSerializer)
    def post(self, request):
         if request.method == 'POST':
                try:
                        session    = request.data['sessionID']
                        semester   = request.data['semester']
                        userID   = request.data['userID']
                        id       = request.data['id']
                        check = Session.objects.filter(id = request.data['sessionID'], userID = request.data['userID'])
                        if(not check):
                            return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)

                        sem = Semester.objects.get(id=id)
                        #print(levels)
                        sem.name = semester
                        sem.sessionID = session
                        sem.userID = userID
                        sem.save()
                        semesterCount = Semester.objects.filter(userID = request.data['userID']).count()
                    
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':semesterCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         
         return Response({'message':'SERVER_ERORR','error':'Request Method Not Allowed', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 

class DeleteSemesterView(APIView):
    def delete(self, request, id, format=None):
        try:  
            instance = Semester.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
             