# accounts/views.py
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer, SemesterUploadSerializer, CoursesUploadSerializer,LevelUploadSerializer,GradeUploadSerializer
from .serializers import FacultyUploadSerializer,DepartmentUploadSerializer, ProgrammeUploadSerializer, StudentRecordsUploadSerializer
from .serializers import ShippingUploadSerializer, CourierUploadSerializer
from .serializers import StudentResultsUploadSerializer, State, SessionUploadSerializer,SaveStudentResultsSerializer,SaveResultOfStudentsSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Users,SchoolSettings, Faculty,Department,Apikeys, Programme,Semester,Courses, Roles, UserRole, Grade,Courier, RolePermissions, Shipping, Level,StudentRecords, StudentResults,Session,ResultOfStudents
from rest_framework.views import APIView
from .utils import generate_otp, send_otp_email
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import datetime
import smtplib
from rest_framework.exceptions import APIException
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from easyaudit.models import CRUDEvent
import io, csv, pandas as pd
from django.shortcuts import redirect
from rest_framework.views import exception_handler
from .email_utils import send_custom_email
from .email_utils import send_email_with_template
import json
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SaveSchoolSettingsSerializer
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

@api_view(['POST'])
def register_user(request):
     
    if request.method == 'POST':
        permission_classes =[]
        serializer = UserSerializer(data=request.data)
        check = Users.objects.filter(email=request.data["email"])
        if(check):
                return Response({"error":"Email already exists","statuscode":208,  'message':'ALREADY_EXIST' },status=status.HTTP_208_ALREADY_REPORTED)

        if serializer.is_valid():
                  
            serializer.save()
            return Response({
                             'email':request.data['username'], 
                             'expireDate':datetime.datetime.now(),
                             'expiresIn': 3600,
                            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
      permission_classes = []
      @swagger_auto_schema(request_body=UserSerializer)
      def post(self, request):
      
        if request.method == 'POST':
            username = request.data['username']
            password = request.data['password']

        user = None
        try:
        
                if '@' in username:
                    username= request.data['username'].rsplit('@', 1)[0]
                    
                if not user:
                    user = authenticate(username=username, password=password)
               
                # if not user:
                #       return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED,message="")

                if user:
                    if user.status == False:
                        return Response({'error': 'Account not active, Please contact administrator', 'message':'NOT_ACTIVATED',}, status=status.HTTP_401_UNAUTHORIZED) 
                        
                    results = Apikeys.objects.filter(createdBy= request.data['username'])
                    print(results)
                    ap = results.values("apikey").first()
                  
                    #get User Roles 
                    ro = UserRole.objects.filter(username=request.data['username'])
                  
                    if ro.exists():
                        role = ro.values('roleID').first()
                        roles = role['roleID']
                    else:
                        roles = 0
                    #print('user I' + user.userID)
                    #Get Department 
                    dept = Department.objects.filter(userID =user.userID).count()
                    fac  = Faculty.objects.filter(userID =user.userID).count()
                    std  = StudentRecords.objects.filter(userID =user.userID).count()
                    #Get School logo  
                   
                    logos = SchoolSettings.objects.filter(userID = user.userID)
                   
                    if logos:
                        logopath = logos.values("logopath").first()
                        sh       = logos.values("shortname").first()
                        
                        if logopath:
                            logo = logopath["logopath"]
                        if sh:
                            shortname =sh["shortname"]
                        
                    if not logos: logo=""
                    if not logos : shortname = ""
                        
                    CRUDEvent.objects.filter()
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key,
                                     'id':user.id,
                                    'email': request.data['username'], 
                                    'userID':user.userID,
                                    'expireDate':datetime.datetime.now(),
                                    'expiresIn': 3600,
                                    'schoolName':user.name,
                                    'idToken':token.key,
                                    'apikey':ap["apikey"],
                                    'role':roles,
                                    'logo':logo,
                                    'department':dept,
                                    'student':std,
                                    'faculty':fac,
                                    'shortname':shortname,
                                    'kind':"identitytoolkit#VerifyPasswordResponse",
                                    'localId':token.key,
                                    'refreshToken':"AMf-vBxknlI7BEle_brkV4ITkKTKrMJkgARhBpzr7_fxw4EAb04jEiNraQNAl7K81Q_ERfZt7vXSemaz6EATF8V7O",
                                    'registered': True
                                    }, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid credentials', 'message':'INVALID_PASSWORD',}, status=status.HTTP_401_UNAUTHORIZED,)   
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

        return Response({'error': 'Invalid credentials', 'message':'INVALID_PASSWORD',}, status=status.HTTP_401_UNAUTHORIZED,)   
# class SchoolSettings(APIView):
#     @swagger_auto_schema(request_body=SaveSchoolSettingsSerializer)
#     def post(self, request):
#         if request.method == 'POST':
#             serializer = SchoolSettingsSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({
#                                  'email':request.data['userID'], 
#                                  'expireDate':datetime.datetime.now(),
#                                  'expiresIn': 3600,
#                                 }, status=status.HTTP_200_OK)
            
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
       
         
         
        def sendActivationEmail(sender):
                   
            url = "https://api.zeptomail.com/v1.1/email";
            token = "Zoho-enczapikey wSsVR60k+R74Wv11nDOuI+hpyl1UBlv0HEl90FTy4nb1GaiT9sc+xhCaDQX1T/QfFWM4RTEWpLkukB9U2jdc290sw18FDyiF9mqRe1U4J3x17qnvhDzOXW5YkhKBL4gOxgponWhpEMEk+g==";
            #client = new SendMailClient({url, token});
            # Define to/from
            sender = sender
            sender_title = "Allan Smith"
            recipient = 'recipient@example.com'

# Create message
            msg = MIMEText("Message text", 'plain', 'utf-8')
            msg['Subject'] =  Header("Sent from python", 'utf-8')
            msg['From'] = formataddr((str(Header(sender_title, 'utf-8')), sender))
            msg['To'] = recipient

# Create server object with SSL option
# Change below smtp.zoho.com, corresponds to your location in the world. 
# For instance smtp.zoho.eu if you are in Europe or smtp.zoho.in if you are in India.
            server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

# Perform operations via server
            server.login('sender@example.com', 'password')
            server.sendmail(sender, [recipient], msg.as_string())
            server.quit()
        def send_email(request):
            subject = request.POST.get("subject", "")
            message = request.POST.get("message", "")
            from_email = request.POST.get("from_email", "")
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, ["admin@example.com"])
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return HttpResponseRedirect("/contact/thanks/")
            else:
                # In reality we'd use a form class
                # to get proper validation errors.
                return HttpResponse("Make sure all fields are entered and valid.")      
class LogoutView(APIView):
      permission_classes = [IsAuthenticated]
      @swagger_auto_schema(request_body=UserSerializer)
      def post(self, request):
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LoginWithOTP(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp  #update OTP Token
        user.save()

        send_otp_email(email, otp)
        # send_otp_phone(phone_number, otp)

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK) 
class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
class Uploader:
    def import_csv(request):
        if request.method == 'POST':
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    Book.objects.create(
                        title=row['title'],
                        author=row['author'],
                        publication_year=row['publication_year'],
                        isbn=row['isbn']
                    )

            return redirect('success_page')  # Redirect to a success page
        else:
            form = CSVImportForm()

        return render(request, 'import.html', {'form': form}) 

class SchoolSettingsView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(request_body=SaveSchoolSettingsSerializer)
    def post(self, request, *args, **kwargs):
        serializer = SaveSchoolSettingsSerializer(data=request.data)
        print(request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({
                                        'userID':request.data['userID'],
                                        'expireDate':datetime.datetime.now(),
                                        'statuscode':200,
                                        'message':'SAVED_SUCCESS',
                                                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
class SaveResultOfStudentsView(APIView):
    @swagger_auto_schema(request_body=SaveResultOfStudentsSerializer)
    def post(self, request):
         try:         
               if request.method == 'POST':
                    serializer = SaveResultOfStudentsSerializer(data=request.data)
                   
                    if serializer.is_valid(raise_exception=True):
                              sessions    =  Session.objects.filter(userID = request.data['userID']).filter(name__contains=request.data["session"]).values('id').get()
                              levels      =  Level.objects.filter(userID = request.data['userID']).filter(name__contains=request.data["level"]).values('id').get()
                              semesters   =  Semester.objects.filter(userID = request.data['userID']).filter(name__contains=request.data["semester"]).values('id').get()
                              departments =  Department.objects.filter(userID = request.data['userID']).filter(name__contains=request.data["department"]).values("id").get()
                              #name_check = StudentResults.objects.filter(name = request.data['name']).filter(userID = request.data['userID'])
                              check = ResultOfStudents.objects.filter(matricno = request.data['matricno']).filter(userID = request.data['userID']).filter(sessionID=sessions['id']).filter(semester = semesters["id"]).filter(level = levels["id"]).filter(coursecode = request.data["coursecode"]).filter(department = departments["id"])           
                              
                              if check:
                                   resultCount = ResultOfStudents.objects.filter(userID = request.data['userID']).count()
                                   return Response({"statuscode":208, 'affectedRows':resultCount, "error":" Result Supplied Already Exist"}, status=status.HTTP_208_ALREADY_REPORTED) 
                              
                              serializer.save()
                              resultCount = ResultOfStudents.objects.filter(userID = request.data['userID']).count()
                              
                         
                              return Response({
                                             'userID':request.data['userID'],
                                             'affectedRows':resultCount, 
                                             'expireDate':datetime.datetime.now(),
                                             'statuscode':200,
                                             'message':'SAVED_SUCCESS',
                                             }, status=status.HTTP_200_OK)                       
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
         except Exception as e:
                return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                 
