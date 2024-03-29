from ..models import Graduationyear, Session, StudentRecords
from ..serializers import SaveGraduationYearSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall


class SaveGraduationYearView(APIView):
    serializer_class =SaveGraduationYearSerializer
    @swagger_auto_schema(request_body=SaveGraduationYearSerializer)
    def post(self, request):
         if request.method == 'POST':
            
            serializer = SaveGraduationYearSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                       
                        check = Session.objects.filter(id = request.data['sessionID'])
                        if(not check):
                            return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)

                        # name_check = Graduationyear.objects.filter(sessionname = request.data['sessionname']).filter(year = request.data['year']).filter(userID = request.data['userID'])
                        
                        # if(name_check):
                        #     return Response({"error":"Record already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
                         
                        name_year = Graduationyear.objects.filter(year = request.data['year']).filter(userID = request.data['userID'])
                        if name_year:
                             return Response({"error":"Year already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
           
                        ses = Session.objects.get(id = request.data['sessionID'])
                        graduation = Graduationyear()
                        graduation.sessionname = ses.name
                        graduation.year =request.data['year']
                        graduation.userID = request.data['userID']
                        graduation.sessionID = request.data['sessionID']
                        graduation.createdBy = request.data["createdBy"]
                        graduation.save()
                       
                        GraduationyearCount = Graduationyear.objects.filter(userID = request.data['userID']).count()
                    
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':GraduationyearCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    def get(self,request,id=None):  
     
                if request.method == 'GET':
                     try:    
                            sql_query = """
                                SELECT gr.id, gr.year, se.name AS session, se.id
                                FROM taasapp_graduationyear gr
                                INNER JOIN taasapp_session se ON gr."sessionID" = se."id"
                                WHERE gr."userID" = %s
                                ORDER BY gr.year;
                    """
                            with connection.cursor() as cursor:
                                cursor.execute(sql_query, [id])
                                if not cursor:
                                    return Response({'message':'NOT_FOUND','data':cursor}) 
                                    
                                results = cursor.fetchall()
                                    # Process the results as needed
                                data = [{'id': row[0], 'year': row[1],'session':row[2],'sessionID':row[3]} for row in results]
                                if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                                if not data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':400}) 
                    # GraduationyearRecords = Graduationyear.objects.filter(userID=id)
                    # return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(GraduationyearRecords.values())}) 
            
                     except Exception as e:
                         return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
class GetStudentSessionsView(APIView):
       def post(self,request):
         if request.method == 'POST': 
                std = StudentRecords.objects.filter(userID=request.data["userID"], matricno=request.data["matricno"]).first()
                if std:
                    entryyear = std.entryyear
                    graduationyear = std.graduationyear
                    userID = request.data["userID"]
                   
                    try:
                        sql_query = """
                        SELECT gd.year, gd.sessionname as session, gd."sessionID" as sessionID FROM taasapp_graduationyear gd
                        WHERE gd."userID"=%s AND year BETWEEN %s AND %s;
                        """
                        with connection.cursor() as cursor:
                            cursor.execute(sql_query, [userID, entryyear, graduationyear])
                            if not cursor:
                                return Response({'message':'NOT_FOUND','data':cursor}) 
                        
                            results = cursor.fetchall()
                        # Process the results as needed
                        data = [{'year': row[0], 'session': row[1],'sessionID':row[2]} for row in results]
                        if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                        if not data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':400}) 
                    except Exception as e:
                        return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                return Response({'message':'NOT_FOUND','error':"No Student Record Found", 'expireDate':datetime.datetime.now(), 'statuscode':'404'}, status=status.HTTP_404_NOT_FOUND) 
       
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class GraduationUpdateView(APIView):
    serializer_class =SaveGraduationYearSerializer
    @swagger_auto_schema(request_body=SaveGraduationYearSerializer)
    def post(self, request):
         if request.method == 'POST':
                try:
                        session  = request.data['sessionID']
                        year     = request.data['year']
                        userID   = request.data['userID']
                        id       = request.data['id']
                        check = Session.objects.filter(id = request.data['sessionID'], userID = request.data['userID'])
                        if(not check):
                            return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)

                        yr = Graduationyear.objects.get(id=id)
                        yr.year      = year
                        yr.sessionID = session
                        yr.userID    = userID
                        yr.save()
                        
                        graduationCount = Graduationyear.objects.filter(userID = request.data['userID']).count()
                    
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':graduationCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         
         return Response({'message':'SERVER_ERORR','error':'Request Method Not Allowed', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 

class DeleteGraduationView(APIView):
    def delete(self, request, id, format=None):
        try:  
            instance = Graduationyear.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            