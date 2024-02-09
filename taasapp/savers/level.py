from ..models import Level,Session
from ..serializers import SaveLevelSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall


class SaveLevelView(APIView):
    serializer_class =SaveLevelSerializer
    @swagger_auto_schema(request_body=SaveLevelSerializer)
    def post(self, request):
         if request.method == 'POST':
             
            serializer = SaveLevelSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
          
                        check = Session.objects.filter(id = request.data['sessionID'], userID = request.data['userID'])
                        if(not check):
                            return Response({"error":"Session Not Exist","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)

                        name_check = Level.objects.filter(name = request.data['name'], sessionID = request.data['sessionID'], userID = request.data['userID'])
                        
                        if(name_check):
                            return Response({"error":"Level already exists for selected session","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)
                    
                             
                        serializer.save()
                        levelCount = Level.objects.filter(userID = request.data['userID']).count()
                    
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':levelCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
        
        
        
    def get(self,request,session=None,id=None):  
            try:
                if request.method == 'GET':
                    levelRecords = Level.objects.filter(sessionID=session,userID=id)
                    return Response({'message':'SAVED_SUCCESS','data':list(levelRecords.values())}) 
            
            except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
 
class ListLevelView(APIView):
     #   @swagger_auto_schema(request_body=SaveDepartmentSerializer)
       def get(self,request,id=None):
         if request.method == 'GET':
              try:    
                    # levelRecords = Level.objects.filter(userID=id)
                    # if not levelRecords:
                    #        return Response({'message':'NOT_FOUND','data':list(levelRecords.values())}) 
               
                    # return Response({'message':'SAVED_SUCCESS','data':list(levelRecords.values())}) 
                sql_query = """
                        SELECT lv.id, lv.name as level, se.name as session  FROM taasapp_level lv INNER JOIN taasapp_session se ON lv."sessionID" = se."id"
                        WHERE lv."userID" =%s;
                        """
                with connection.cursor() as cursor:
                    cursor.execute(sql_query, [id])
                    if not cursor:
                        return Response({'message':'NOT_FOUND','data':cursor}) 
                        
                    results = cursor.fetchall()
                        # Process the results as needed
                    data = [{'id': row[0], 'level': row[1],'session':row[2]} for row in results]
                    if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                    if not data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':400}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        