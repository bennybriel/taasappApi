from ..models import StudentRecords,ResultOfStudents, SemesterResult
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from ..utils import dictfetchall

class GetStudentInformationList(APIView):
       def post(self,request):
         if request.method == 'POST':

             print(request.data)
             try:
                  userID   = request.data['userID']
                  matricno = request.data['matricno']
                  
                  studentrecords = StudentRecords.objects.filter(userID=userID).filter(matricno=matricno)
                
                  if not studentrecords:
                        return Response({'message':'NOT_FOUND','statuscode':400}) 
               
                  return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(studentrecords.values())}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(status=status.HTTP_400_BAD_REQUEST) 

class GenerateTranscriptView(APIView):
       def post(self,request):
         if request.method == 'POST':
             try:
                  userID   = request.data['userID']
                  matricno = request.data['matricno']
                  
                  studentrecords = ResultOfStudents.objects.filter(userID=userID).filter(matricno=matricno)
                
                  if not studentrecords:
                        return Response({'message':'No Record Found','statuscode':400}) 
                  
                  # sql_query = """
                  #       SELECT DISTINCT rs.matricno,sm.name as semester,se.name as session,rs."levelID",score,rs.coursecode,point,grade,
                  #       rs."userID", rs.departmentcode,cs.coursetitle,cm.courseunit, st.dob, st.surname,st.firstname,st.othername,
                  #       st.gender,st.phone,st.email,st.cgpa,st.graduationyear,st.entryyear, sr.gpa, sr.cgpa,
                  #       (SELECT name as degreeclass FROM  public.taasapp_degreeclass WHERE id = st.degreeofclass),
                  #       (SELECT name as department  FROM public.taasapp_department WHERE departmentcode = rs.departmentcode),
                  #       (SELECT fa.name as faculty  FROM public.taasapp_faculty fa INNER JOIN public.taasapp_department dt ON fa.facultycode = dt.facultycode  WHERE dt.departmentcode =rs.departmentcode)
                  #       FROM public.taasapp_resultofstudents rs
                  #       INNER JOIN public.taasapp_session se ON rs."sessionID" = se."id"
                  #       INNER JOIN public.taasapp_semester sm ON rs."semesterID" = sm."id"
                  #       INNER JOIN public.taasapp_courses cs ON rs.coursecode=cs.coursecode
                  #       INNER JOIN public.taasapp_curriculum cm ON rs.coursecode=cm.coursecode
                  #       INNER JOIN public.taasapp_studentrecords st ON rs.matricno = st.matricno
                  #       INNER JOIN public.taasapp_semesterresult sr ON rs.matricno = sr.matricno
                  #       WHERE rs.matricno= %s AND rs."userID" = %s;
                  #       """
                  # with connection.cursor() as cursor:
                  #       cursor.execute(sql_query, [matricno, userID])
                  #       if not cursor:
                  #             return Response({'message':'No Record Found','data':cursor}) 
                        
                  #       results = cursor.fetchall()
                  #       # Process the results as needed
                  #       data = [ {
                  #                 'matricno': row[0], 'semester':row[1],'session':row[2],'level':row[3],'score':row[4],
                  #                 'coursecode':row[5],'point':row[6], 'grade':row[7],'userID':row[8], 'departmentcode':row[9],
                  #                 'coursetitle': row[10], 'courseunit':row[11],'dob':row[12],'surname':row[13],'firstname':row[14],
                  #                 'othername': row[15], 'gender':row[16],'phone':row[17],'email':row[18],'cgpa':row[19],
                  #                 'graduationyear': row[20], 'entryyear':row[21],'gpa':row[22],'scpga':row[23],'degreeclass':row[24],'department':row[25],'faculty':row[26],
                  #                } 
                                
                  #               for row in results]
                  
                  
                  sql_query = """
                        SELECT rs.matricno, sm.name as semester, se.name as session, rs."levelID", score, rs.coursecode, point, grade,
                        rs."userID", rs.departmentcode, cs.coursetitle, cm.courseunit, st.dob, st.surname, st.firstname, st.othername,
                        st.gender, st.phone, st.email, st.cgpa, st.graduationyear, st.entryyear, sr.gpa, sr.cgpa,se.id as sessionid,sm.id as semesterid,
                        (SELECT name as degreeclass FROM public.taasapp_degreeclass WHERE id = st.degreeofclass),
                        (SELECT name as department FROM public.taasapp_department WHERE departmentcode = rs.departmentcode AND rs."userID"=taasapp_department."userID")
                        
                        FROM public.taasapp_resultofstudents rs
                        INNER JOIN public.taasapp_session se ON rs."sessionID" = se."id"
                        INNER JOIN public.taasapp_semester sm ON rs."semesterID" = sm."id"
                        INNER JOIN public.taasapp_courses cs ON rs.coursecode=cs.coursecode
                        INNER JOIN public.taasapp_curriculum cm ON rs.coursecode=cm.coursecode
                        INNER JOIN public.taasapp_studentrecords st ON rs.matricno = st.matricno
                        LEFT JOIN public.taasapp_semesterresult sr ON rs.matricno = sr.matricno
                        WHERE rs.matricno = %s AND rs."userID" = %s 
                        ORDER BY se.name ASC;
                        """

                        # (SELECT fa.name as faculty FROM public.taasapp_faculty fa INNER JOIN public.taasapp_department dt ON fa.facultycode = dt.facultycode
                        # WHERE taasapp_department.departmentcode = rs.departmentcode AND taasapp_department."userID" = rs."userID")
                  with connection.cursor() as cursor:
                        cursor.execute(sql_query, [matricno, userID])
                        results = cursor.fetchall()

                        if not results:
                              return Response({'message': 'No Record Found', 'data': results})

                        # Process the results as needed
                        data = [{
                              'matricno': row[0], 'semester': row[1], 'session': row[2], 'level': row[3], 'score': row[4],
                              'coursecode': row[5], 'point': row[6], 'grade': row[7], 'userID': row[8], 'departmentcode': row[9],
                              'coursetitle': row[10], 'courseunit': row[11], 'dob': row[12], 'surname': row[13], 'firstname': row[14],
                              'othername': row[15], 'gender': row[16], 'phone': row[17], 'email': row[18], 'cgpa': row[19],
                              'graduationyear': row[20], 'entryyear': row[21], 'gpa': row[22], 'scpga': row[23],'sessionid':row[24],'semesterid':row[25],'degreeclass': row[26], 'department': row[27],
                        } for row in results]

                        if data: return Response({'message':'FETCH_SUCCESS','data':data,'statuscode':200}) 
                        if not data: return Response({'message':'No Record Found','error':'No Record Found', 'data':data,'statuscode':400}) 
                  
                  return Response({'message':'No Record Found','data':results}) 
                  
               
                  return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(studentrecords.values())}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(status=status.HTTP_400_BAD_REQUEST)   


class GetSemesterResultsView(APIView):
       def post(self,request):
         if request.method == 'POST':

             print(request.data)
             try:
                  userID   = request.data['userID']
                  matricno = request.data['matricno']
                  # semester = request.data['semester']
                  # session  = request.data['session']
                  # level    = request.data['level']
                    
                  sResult = SemesterResult.objects.filter(userID=userID).filter(matricno=matricno)
                
                  if not sResult:
                        return Response({'message':'NOT_FOUND','statuscode':400}) 
               
                  return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(sResult.values())}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(status=status.HTTP_400_BAD_REQUEST) 
