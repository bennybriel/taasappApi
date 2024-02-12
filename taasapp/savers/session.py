from ..models import Session
from ..serializers import SaveSessionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from ..authenticateHeader import authenticate_user
from ..checkers import check_session_existence
class SaveSessionView(APIView):
    serializer_class =SaveSessionSerializer
    @swagger_auto_schema(request_body=SaveSessionSerializer)
    def post(self, request):
         if request.method == 'POST':
              try:
                    serializer = SaveSessionSerializer(data=request.data)
                    authenticated, response = authenticate_user(request, request.data["userID"])
                    # If authentication failed, return the response
                    if not authenticated:
                        return response      
                   
                    if serializer.is_valid():
                         name_check = Session.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
                        
                         if(name_check):
                              return Response({"error":"Name already exists","statuscode":208,  'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)
                         
                     
                         serializer.save()
                         sessionCount = Session.objects.filter(userID = request.data['userID']).count()
                    
                         return Response({
                                        'userID':request.data['userID'],
                                        'affectedRows':sessionCount, 
                                        'expireDate':datetime.datetime.now(),
                                        'message':'SAVED_SUCCESS',
                                        'statuscode':200,
                                        }, status=status.HTTP_200_OK)
              except Exception as e:
                     return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
    
    def get(self,request,id=None):
         if request.method == 'GET':
              try:    
                    sessionRecords = Session.objects.filter(userID=id)
                    if not sessionRecords:
                           return Response({'message':'NOT_FOUND','data':list(sessionRecords.values())}) 
               
                    return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(sessionRecords.values())}) 
              except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
            


class GetStudentSessionView(APIView):
       def post(self,request):
         if request.method == 'POST':
                matricno= request.data['matricno']
                
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



class SessionUpdateView(APIView):
    serializer_class =SaveSessionSerializer
    @swagger_auto_schema(request_body=SaveSessionSerializer)
    def post(self, request):
         if request.method == 'POST':
                try:
                       
                        name              = request.data['name']
                        userID            = request.data['userID']
                        id                = request.data['id']
                        
                           
                        if check_session_existence(request):
                               return Response({"error": "Session already exists","statuscode": 208,"message": 'ALREADY_EXIST'}, status=status.HTTP_208_ALREADY_REPORTED)
                               
                        sess = Session.objects.get(id=id)
                        sess.name = name
                        sess.save()
                        sessionCount =Session.objects.filter(userID = userID).count()
                        return Response({
                                    'userID':request.data['userID'],
                                    'affectedRows':sessionCount, 
                                    'expireDate':datetime.datetime.now(),
                                    'statuscode':200,
                                    'message':'SAVED_SUCCESS',
                                    }, status=status.HTTP_200_OK)
                    
                  
                except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
         
         return Response({'message':'SERVER_ERORR','error':'Request Method Not Allowed', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_400_BAD_REQUEST) 


class DeleteSessionView(APIView):
    def delete(self, request, id, format=None):
        try: 
          
            instance = Session.objects.get(id=id)  
            instance.delete()
            return Response({'message':'DELETED','error':"Record deleted successfully"}) 
        except Exception as e:
             return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return Response({'message':'SERVER_ERORR', 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            