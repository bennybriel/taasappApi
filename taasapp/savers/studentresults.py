from ..models import ResultOfStudents, SemesterResult
from ..serializers import SaveResultOfStudentsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime  
from drf_yasg.utils import swagger_auto_schema

class SaveResultOfStudentsView(APIView):
    serializer_class =SaveResultOfStudentsSerializer
    @swagger_auto_schema(request_body=SaveResultOfStudentsSerializer)
    def post(self, request):
         try:         
               if request.method == 'POST':
                    serializer = SaveResultOfStudentsSerializer(data=request.data)
                    scores      = request.POST.getlist("score[]")
                    matricno = request.data.get("matricno", "")
                    semester = request.data.get("semesterID", "")
                    session = request.data.get("sessionID", "")
                    level    = request.data.get("levelID", "")
                    userID    = request.data.get("userID", "")
                    createdBy = request.data.get("createdBy", "")
                    departmentcode = request.data.get("departmentcode", "")
                    grade = '' 
                    for i, score in enumerate(scores):
                        # Retrieve the coursecode list using the current index
                         course_code_list = request.POST.getlist(f"coursecode[{i}][coursecode]")     
                         # Create a new instance of your model
                         results= ResultOfStudents()
                         points, grade = self.get_point(score, grade)
                         # Populate the fields with data
                         results.coursecode =  course_code_list[0]
                         results.score = score
                         results.matricno = request.data.get("matricno", "")
                         results.semesterID = request.data.get("semesterID", "")
                         results.sessionID = request.data.get("sessionID", "")
                         results.levelID = request.data.get("levelID", "")
                         results.departmentcode = request.data.get("departmentcode", "")
                         results.userID = request.data.get("userID", "")
                         results.createdBy = request.data.get("createdBy", "")
                         results.point = points
                         results.grade = grade 

                        # Save the instance to the database
                         check = ResultOfStudents.objects.filter(matricno = request.data['matricno']).filter(userID = request.data['userID']).filter(sessionID=request.data['sessionID']).filter(semesterID = request.data["semesterID"]).filter(levelID = request.data["levelID"]).filter(coursecode = course_code_list[0]).filter(departmentcode = request.data["departmentcode"])              
                         if not check:
                              results.save()
                              self.semesterResults(
                                    request.data["matricno"],
                                    request.data.get("semesterID", ""),
                                    request.data.get("sessionID", ""),
                                    request.data.get("levelID", ""),
                                    request.data.get("cgpa", ""),
                                    request.data.get("gpa", ""),
                                    request.data.get("departmentcode", ""),
                                    request.data.get("userID", ""),
                                    request.data.get("createdBy", "")
                                    )
                         if check:
                              result = ResultOfStudents.objects.get(matricno=matricno,sessionID=session,semesterID=semester,levelID=level,departmentcode=departmentcode,coursecode =course_code_list[0], userID=userID)
                              result.score = score
                              result.point = points
                              result.grade = grade 
                              result.save()
                              #Update Semester Results
                              self.semesterResults(
                                    request.data["matricno"],
                                    request.data.get("semesterID", ""),
                                    request.data.get("sessionID", ""),
                                    request.data.get("levelID", ""),
                                    request.data.get("cgpa", ""),
                                    request.data.get("gpa", ""),
                                    request.data.get("departmentcode", ""),
                                    request.data.get("userID", ""),
                                    request.data.get("createdBy", "")
                                    )
                             
                    allresult =  ResultOfStudents.objects.filter( matricno   = request.data['matricno'], 
                                                               userID     = request.data['userID'],
                                                               sessionID  = request.data['sessionID'],
                                                               semesterID = request.data["semesterID"],
                                                               levelID    = request.data["levelID"],
                                                               departmentcode = request.data["departmentcode"])
                    # print(allresult)
                    resultCount = ResultOfStudents.objects.filter(userID = request.data['userID']).count()
                    return Response({
                                             'userID':request.data['userID'],
                                             'affectedRows':resultCount, 
                                             'result':list(allresult.values()),
                                             'expireDate':datetime.datetime.now(),
                                             'statuscode':200,
                                             'message':'SAVED_SUCCESS',
                                             }, status=status.HTTP_200_OK)                       
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
     
    def get_point(self, score, grade):
        try:
            score = int(score)

            if score >= 70:
                grade = 'A'
                return 5, grade
            elif score >= 60:
                grade = 'B'
                return 4, grade
            elif score >= 50:
                grade = 'C'
                return 3, grade
            elif score >= 45:
                grade = 'D'
                return 2, grade
            elif score >= 40:
                grade = 'E'
                return 1, grade
            else:
                grade = 'F'
                return 0, grade
        except (ValueError, TypeError):
            return 0, 'Invalid score'
    def semesterResults(self, matricno, semesterID,sessionID,level,cgpa,gpa,departmentcode,userID,createdBy):
          semeResult= SemesterResult(matricno =matricno)
          semeResult.matricno   = matricno
          semeResult.level      = level
          semeResult.sessionID  = sessionID
          semeResult.semesterID = semesterID
          semeResult.departmentcode= departmentcode
          semeResult.gpa        = gpa
          semeResult.cgpa       = cgpa
          semeResult.userID     = userID
          semeResult.createdBy  = createdBy
          
          check  = SemesterResult.objects.filter(matricno=matricno, 
                                                 semesterID=semesterID,
                                                 sessionID=sessionID,
                                                 level=level,
                                                 departmentcode=departmentcode,
                                                 userID = userID)
       
          if not check: semeResult.save()
          if check:
                result = SemesterResult.objects.get(matricno=matricno,sessionID=sessionID,semesterID=semesterID,level=level,departmentcode=departmentcode,userID=userID)
                result.gpa  = gpa
                result.cgpa = cgpa
                result.save()    
               
                    

class GetStudentResultsView(APIView):
       def post(self,request):
         if request.method == 'POST':

             print(request.data)
             try:
                  userID   = request.data['userID']
                  matricno = request.data['matricno']
                  semester = request.data['semesterID']
                  session  = request.data['sessionID']
                  level    = request.data['levelID']
                  # = request.data["departmentcode"]
                    
                  sResult = ResultOfStudents.objects.filter(userID=userID,
                                                            matricno=matricno,
                                                            semesterID = semester,
                                                            sessionID=session,
                                                            levelID=level,
                                                            )
                
                  if not sResult:
                        return Response({'message':'NOT_FOUND','statuscode':400}) 
               
                  return Response({'message':'SAVED_SUCCESS','statuscode':200,'data':list(sResult.values())}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
           
         return Response(status=status.HTTP_400_BAD_REQUEST) 

