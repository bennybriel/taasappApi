from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
# Create your models here.
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.db import models
import os
class Users(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('standard', 'Standard User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='standard')
    email = models.EmailField(unique=True,max_length=100)
    username= models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    status = models.BooleanField()
    isschool = models.BooleanField()
    userID = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    othername = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Add the otp field here
    ipaddress = models.CharField(max_length=20, null=True, blank=True)  # 
    email_verified = models.BooleanField(default=False)
    isapikey = models.BooleanField(default=True)
    apikey= models.CharField(max_length=200, unique=True)
    USERNAME_FIELD='username'
    
    #USERNAME_FIELD
    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    
def logo_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "%s.%s"% (instance.userID, extension)
    return new_filename
class SchoolSettings(models.Model):
    logopath= models.ImageField(upload_to=logo_dir_path)
    city =  models.CharField(max_length=100)
    slogan = models.CharField(max_length=100)
    shortname = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)

    def __str__(self):
        return self.shortname
class Faculty(models.Model):
    name        = models.CharField(max_length=100)
    facultycode = models.CharField(max_length=100)
    createdBy   = models.CharField(max_length=100)
    userID      = models.CharField(max_length=100)
    createdAt   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    facultycode = models.CharField(max_length=100)
    departmentcode = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Programme(models.Model):
    name = models.CharField(max_length=100)
    facultycode = models.CharField(max_length=100)
    programmecode = models.CharField(max_length=100)
    departmentcode = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Grade(models.Model):
    minscore = models.IntegerField()
    maxscore = models.IntegerField()
    point = models.FloatField()
    grade = models.CharField(max_length=10)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.grade
class Semester(models.Model):
    name = models.CharField(max_length=100)
    sessionID = models.IntegerField()
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
   
    
    def __str__(self):
        return self.name

class Level(models.Model):
    name      = models.IntegerField()
    sessionID = models.IntegerField()
    createdBy = models.CharField(max_length=100)
    userID    = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userID
class RoleTypes(models.Model):
    name = models.CharField(max_length=100)
    #roleID = models.IntegerField()
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    # userID=models.ForeignKey(Users, on_delete=models.CASCADE, related_name='roletypes_createdBy')
    # createdBy=models.ForeignKey(Users, on_delete=models.CASCADE, related_name='roletypes_userID')
   
    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=100)
    countryID = models.IntegerField()
    country  =  models.CharField(max_length=100)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class LGA(models.Model):
    name = models.CharField(max_length=100)
    stateID = models.IntegerField()
    countryID = models.IntegerField()
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
class Session(models.Model):
    name = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
    
class Courses(models.Model):
    coursecode  = models.CharField(max_length=20)
    coursetitle = models.CharField(max_length=200)
    createdBy   = models.CharField(max_length=100)
    userID      = models.CharField(max_length=100)
    createdAt   = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.coursetitle
class Curriculum(models.Model):
    coursecode      = models.CharField(max_length=20)
    departmentcode  = models.CharField(max_length=20)
    coursestatus    = models.CharField(max_length=20)
    #description     = models.CharField(max_length=100)
    courseunit      = models.IntegerField()
    session         = models.IntegerField()
    semester        = models.IntegerField()
    level           = models.IntegerField()
    createdBy       = models.CharField(max_length=100)
    userID          = models.CharField(max_length=100)
    createdAt       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coursecode
class StudentRecords(models.Model):
    matricno  = models.CharField(max_length=50)
    surname   = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    othername = models.CharField(max_length=20)
    dob       = models.DateField()
    gender    = models.CharField(max_length=10)
    phone     = models.CharField(max_length=11)
    address   = models.CharField(max_length=200)
    email     = models.CharField(max_length=100)                          
    graduationyear = models.IntegerField()
    cgpa      =  models.DecimalField(decimal_places=2,max_digits=5)
    degreeofclass   = models.IntegerField()
    countryID = models.IntegerField()
    entryyear = models.IntegerField()
    departmentcode = models.CharField(max_length=20)
    facultycode = models.CharField(max_length=20)
    stateID = models.IntegerField()
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.matricno
    
class StudentResults(models.Model):
    matricno = models.CharField(max_length=50)
    semester = models.IntegerField()
    department = models.IntegerField()
    faculty  = models.IntegerField()
    level = models.IntegerField()
    score = models.IntegerField()
    coursecode = models.CharField(max_length=20)
    point = models.FloatField()
    grade = models.CharField(max_length=5)                        
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    sessionID= models.IntegerField()
    createdAt = models.DateTimeField(auto_now=True)
       
    def __str__(self):
        return self.matricno

class Courier(models.Model):
    #courierID = models.IntegerField()
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Shipping(models.Model):
    location = models.CharField(max_length=100)
    courierID = models.IntegerField()
    countryID = models.IntegerField()
    cost = models.FloatField()
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.location
    


class ResultOfStudents(models.Model):
    matricno = models.CharField(max_length=50)
    semesterID = models.CharField()
    departmentcode = models.CharField(max_length=50)
    levelID = models.IntegerField()
    score = models.IntegerField()
    coursecode = models.CharField(max_length=20)
    point = models.FloatField()
    grade = models.CharField(max_length=5)                                
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    sessionID= models.IntegerField()
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.matricno
class SemesterResult(models.Model):
    matricno = models.CharField(max_length=50)
    semesterID = models.CharField()
    departmentcode = models.CharField(max_length=50)
    level = models.IntegerField()   
    gpa = models.FloatField()
    cgpa = models.FloatField()                           
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    sessionID= models.IntegerField()
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.matricno
    
class StudentTranscript(models.Model):
    matricno = models.CharField(max_length=50)
    semesterID = models.IntegerField()
    levelID = models.IntegerField()
    score = models.IntegerField()
    coursecode = models.CharField(max_length=20)
    point = models.FloatField()
    grade = models.CharField(max_length=5)   
    semester = models.CharField(max_length=100)     
    department = models.CharField(max_length=100) 
    level = models.CharField(max_length=100) 
    academicsession = models.CharField(max_length=100)                              
    createdBy = models.CharField(max_length=100)
    userID = models.CharField(max_length=100)
    sessionID= models.IntegerField()
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.matricno
class Module(models.Model):
    name = models.CharField(max_length=50)
    userID = models.CharField(max_length=100)
class Permissions(models.Model):
    name = models.CharField(max_length=50)
    createdBy = models.CharField(max_length=50)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)


class Roles(models.Model):
    name = models.CharField(max_length=50)
    userID = models.CharField(max_length=50)
    createdBy = models.CharField(max_length=50)
    userID = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now=True)
class UserRole(models.Model):
    roleID    = models.IntegerField()
    username  = models.CharField(max_length=100)
    userID    = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now=True)
    # user = models.OneToOneField(Users, on_delete=models.CASCADE)
    # role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)

class RolePermissions(models.Model):
    roleID = models.IntegerField()
    permissionID = models.IntegerField()
    description = models.CharField(max_length=50)
    userID = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now=True)

class Graduationyear(models.Model):
    year           = models.IntegerField()
    sessionID      = models.IntegerField()
    sessionname  = models.CharField(max_length=100)
    userID    = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Degreeclass(models.Model):
    name        = models.CharField(max_length=100)
    createdBy   = models.CharField(max_length=100)
    # status      = models.BooleanField(default=True)
    userID      = models.CharField(max_length=100)
    createdAt   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class APIKey(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    school = models.CharField(max_length=40)  
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKeyToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.key

class Apikeys(models.Model):
    apikey      = models.CharField(max_length=100)
    isapikey    = models.BooleanField(default=True)
    userID      = models.CharField(max_length=100)
    createdBy   = models.CharField(max_length=50)
    createdAt   = models.DateTimeField(auto_now=True)