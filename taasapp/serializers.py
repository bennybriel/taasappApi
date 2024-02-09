# accounts/serializers.py

from rest_framework import serializers
from .models import Users,SchoolSettings, Permissions,RolePermissions,UserRole, Apikeys,  Degreeclass,Curriculum,Faculty,Department, Programme, Semester,Courses, StudentRecords, StudentResults,Session
from .models import Courier, Shipping, Grade,Level, SemesterResult, Apikeys,UserRole, Graduationyear, Country, State,ResultOfStudents,StudentTranscript, Roles,UserRole
import datetime
import uuid
#from .signals import send_email_verification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password','ipaddress','name']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = Users(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name']
        )
        userID =uuid.uuid4()
        user.last_login=datetime.datetime.now()
        user.ipaddress = validated_data['ipaddress']
        user.is_active =True
        user.status=False
        user.isschool = True
        user.first_name = validated_data['name']
        user.last_name  = validated_data['name']
        user.email_verified=False
        user.userID = userID
        user.set_password(validated_data['password'])
        user.save()
        if user:
             checkApi= Apikeys.objects.filter(userID=userID)
             if not checkApi:
                api = Apikeys()
                api.apikey = uuid.uuid4()
                api.userID = userID
                api.createdBy = validated_data['email']
                api.save()
                
             checkRole = UserRole.objects.filter(userID=userID)
             if not checkRole:
                role = UserRole()
                role.roleID="2"
                role.username = validated_data['email']
                role.createdBy =validated_data['email']
                role.userID = userID
                role.save()
             return user
         
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'password','first_name','last_name','userID','ipaddress','phone','email','username']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        
        user = Users(
            userID=validated_data['userID'],
             username=validated_data['username'],
            email=validated_data['email'],
        )
        user.name =validated_data['name']
        user.last_login =  datetime.datetime.now()
        user.ipaddress  =  validated_data['ipaddress']
        user.first_name =  validated_data['first_name']
        user.last_name  =  validated_data['last_name']
        user.status = True
        user.isschool = False
        user.email_verified=False
        user.is_staff = True;
        user.is_active =True
        user.userID = validated_data['userID']
        user.name   = validated_data['name']
        user.phone  = validated_data['phone']
        user.set_password(validated_data['phone'])
        user.save()

        return user


class FacultyUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
class SaveFacultyFileSerializer(serializers.Serializer):
    class Meta:
        model = Faculty
        fields = "__all__"
class DepartmentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
class ProgrammeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)   
class SemesterUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)   
class LevelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)  
class GradeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)  
class ShippingUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)  
class CourierUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)  
class SaveSemesterFileSerializer(serializers.Serializer):
     class Meta:
        model = Semester
        fields = "__all__" 
class CoursesUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
class CurriculumUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
class SaveCoursesFileSerializer(serializers.Serializer):
     class Meta:
        model = Courses
        fields = ['courescode','coursetitle','courseunit','createdBy','userID']
class StudentRecordsUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
class SemesterResultsUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)    
class SaveStudentRecordsFileSerializer(serializers.Serializer):
     class Meta:
        model = StudentRecords
        fields = ["__all__"]
class StudentResultsUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
class SaveStudentResultsFileSerializer(serializers.Serializer):
     class Meta:
        model = StudentRecords
        fields = "__all__"
 
class SessionUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    createdBy = serializers.CharField(max_length=100)
    userID = serializers.CharField(max_length=100)
    
class SaveSessionFileSerializer(serializers.Serializer):
     class Meta:
        model = Session
        fields = "__all__"
        

class SaveFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"
        
        name      = serializers.CharField(max_length =100)
        facultycode = serializers.CharField(max_length =100)
        createdBy = serializers.CharField(max_length=100)
        userID    = serializers.CharField(max_length=100)


class SaveDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name','userID','createdBy','facultycode','departmentcode']
        
   
       

class SaveProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme
        fields = ['name','createdBy','userID','departmentcode','facultycode','programmecode']


class SaveSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"
        
        name      = serializers.CharField(max_length =100)
        #semesterID = serializers.IntegerField()
        createdBy = serializers.CharField(max_length=100)
        userID    = serializers.CharField(max_length=100)

class SaveCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['coursecode','coursetitle','createdBy','userID','description']
        

class SaveCurriculumSerializer(serializers.ModelSerializer):
     class Meta:
        model = Curriculum
        fields = ['coursecode','courseunit','coursestatus','departmentcode','semester','level','createdBy','userID','session']
     

class SaveStudentRecordsSerializer(serializers.ModelSerializer):
        class Meta:
            model = StudentRecords
            fields =[
                    'matricno',
                    'surname',
                    'firstname',
                    'gender',
                    'countryID',
                    'degreeofclass',
                    'stateID',
                    'phone',
                    #'dob',
                    'address',
                    'email',
                    'cgpa',
                    'entryyear',
                    'departmentcode',
                    'facultycode',
                    'graduationyear',
                    'createdBy',
                    'userID'
            ]


        
class SaveStudentResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResults
        fields = "__all__"
        
    def create(self, validated_data):
        return StudentResults.objects.create(**validated_data)
            
class SaveResultOfStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultOfStudents
        fields =[
                    'matricno',
                    'semesterID',
                    'departmentcode',
                    'levelID',
                    'score',
                    'coursecode',
                    'point',
                    'grade',
                    'sessionID',
                    'createdBy','userID'
            ]
        
    def create(self, validated_data):
        return ResultOfStudents.objects.create(**validated_data)
            

class SaveSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
        
        name      = serializers.CharField(max_length =100)
        #sessionID = serializers.IntegerField()
        createdBy = serializers.CharField(max_length=100)
        userID    = serializers.CharField(max_length=100)

class SaveCourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = "__all__"
        
        name      = serializers.CharField(max_length =100)
        address      = serializers.CharField(max_length =100)
        phone      = serializers.CharField(max_length =100)
        email      = serializers.CharField(max_length =100)
        createdBy = serializers.CharField(max_length=100)
        userID    = serializers.CharField(max_length=100)
class SaveShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['location','cost','createdBy','userID','courierID','countryID']
        

class SaveGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
        
        minscore      = serializers.IntegerField()
        maxscore      = serializers.IntegerField()
        grade         = serializers.CharField(max_length =10)
        point         = serializers.FloatField()
        createdBy     = serializers.CharField(max_length=100)
        userID        = serializers.CharField(max_length=100)

class SaveLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"
        
        name      = serializers.CharField(max_length =100)
        sessionID = serializers.IntegerField()
        createdBy = serializers.CharField(max_length=100)
        userID    = serializers.CharField(max_length=100)

class SaveSchoolSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolSettings
        #fields = "__all__"
        fields =['userID','slogan','city','country','address','createdBy','phone','logopath','shortname','state']
    
    
class SaveCountrySerializer(serializers.ModelSerializer):
     class Meta:
        model = Country
        fields = "__all__"
        
        name        = serializers.CharField(max_length =100)
        countryID   = serializers.IntegerField()
        createdBy   = serializers.CharField(max_length=100)
        userID      = serializers.CharField(max_length=100)


    
class SaveStateSerializer(serializers.ModelSerializer):
     class Meta:
        model = State
        fields = ['name','country','userID','createdBy']
        
class SaveRolesSerializer(serializers.ModelSerializer):
     class Meta:
        model = Roles
        fields ='__all__'

class SaveUserRoleSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserRole
        fields = ['roleID','userID','createdBy','username']
class SaveGraduationYearSerializer(serializers.ModelSerializer):
     class Meta:
        model = Graduationyear
        # fields ='__all__'
        fields = ['userID','createdBy','year','sessionID']
class SaveDegreeClassSerializer(serializers.ModelSerializer):
     class Meta:
        model = Degreeclass
        fields ='__all__'

class SaveSemesterResultSerializer(serializers.ModelSerializer):
     class Meta:
        model = SemesterResult
        fields ='__all__'
class SavePermissionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Permissions
        fields ='__all__'

class SaveRolePermissionSerializer(serializers.ModelSerializer):
     class Meta:
        model = RolePermissions
        fields ='__all__'

class SchoolActivatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email','status','userID']
    #----------------------


class SaveApikeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apikeys
        fields = ['apikey','createdBy','userID']
    #----------------------