
#SAVES
from django.urls import path
from .views import register_user, LoginView, LogoutView, LoginWithOTP
from .views import ValidateOTP
from .views  import SaveResultOfStudentsView
from .views import SchoolSettingsView
from  rest_framework.schemas import get_schema_view
from . signals import AccountActivationView
from . savers.faculty import SaveFacultyView, DeleteFacultyView
from . savers.faculty import SaveFacultyView
from . savers.department import SaveDepartmentView, ListDepartmentView,DepartmentUpdateView,DeleteDepartmentView
from . savers.programme import SaveProgrammeView, ListProgrammeView,ProgrammeUpdateView, DeleteProgrammeView
from . savers.semester import SaveSemesterView
from . savers.studentrecords import SaveStudentRecordsView, GetStudentInformationLists
from . savers.courses import SaveCoursesView 
from . savers.session import SaveSessionView, SessionUpdateView, DeleteSessionView
from . savers.courier import SaveCourierView
from . savers.shipping import SaveShippingView
from . savers.grade import SaveGradeView
from . savers.level import SaveLevelView, ListLevelView, LevelUpdateView,DeleteLevelView
from . savers.schoolsettings import SaveSchoolSettingView
from . savers.country import SaveCountryView
from . savers.state import SaveStateView
from . search.searchstudentrecords import GetStudentInformationList
from . savers.studentresults import SaveResultOfStudentsView,GetStudentResultsView
from . savers.resetApikey import ResetApiKeyView
from . savers.roles import SaveRolesView
from . savers.users import SaveUsersView, ListSchoolAccountView, DeleteUsersView
from . savers.userrole import SaveUsersRoleView, ListUserRolesView
from . savers.activate import ActivateSchoolView
from . savers.graduationyear import SaveGraduationYearView,GetStudentSessionsView
from . savers.degreeclass import SaveDegreeclassView
from . savers.curriculum import SaveCurriculumView, GetStudentCoursesView
from . savers.semesterresult import SaveSemesterResultView
from . savers.permission import SavePermissionsView
from . savers.rolepermission import SaveRolePermissionView
from . savers.changelogo import SaveChangeLogoView
#Uploader
from . uploaders.facultupload import FacultyFileUploaderView
from . uploaders.departmentupload import DepartmentFileUploaderView
from . uploaders.programmeupload import ProgrammeFileUploaderView
from . uploaders.semesterupload import SemesterFileUploaderView
from . uploaders.courseupload import CoursesFileUploaderView
from . uploaders.curriculumupload import CurriculumFileUploaderView
from . uploaders.levelupload import LevelFileUploaderView
from . uploaders.sessionupload import SessionFileUploaderView
from . uploaders.courierupload import CourierFileUploaderView
from . uploaders.shippingupload import ShippingFileUploaderView
from . uploaders.gradeupload import GradeFileUploaderView
from . uploaders.studentrecordupload import StudentRecordFileUploaderView
from . uploaders.resultofstudents import StudentResultsFileUploaderView
from . uploaders.semesterresultupload import SemesterResultsFileUploaderView

from . search.searchstudentrecords import GenerateTranscriptView, GetSemesterResultsView

urlpatterns = [
    #Auth And Register
    path('register/', register_user, name='register'),
    path('login/', LoginView.as_view()),
    path('saveusers/', SaveUsersView.as_view()),
    path('saveusers/<str:id>/', SaveUsersView.as_view()),
    path('resetkey/', ResetApiKeyView.as_view()),
    path('resetkey/<str:id>/', ResetApiKeyView.as_view()),
    #Upload URL
    path('facultyupload/', FacultyFileUploaderView.as_view()),
    path('departmentupload/', DepartmentFileUploaderView.as_view()),
    path('programmeupload/',  ProgrammeFileUploaderView.as_view()),
    path('semesterupload/',   SemesterFileUploaderView.as_view()),
    path('coursesupload/',    CoursesFileUploaderView.as_view()),  
    path('curriculumsupload/',    CurriculumFileUploaderView.as_view()),  
    path('studentrecordsupload/',    StudentRecordFileUploaderView.as_view()),
    path('studentresultsupload/',    StudentResultsFileUploaderView.as_view()),
    path('sessionupload/',    SessionFileUploaderView.as_view()),
    path('levelupload/', LevelFileUploaderView.as_view()),
    path('gradeupload/', GradeFileUploaderView.as_view()),
    path('courierupload/', CourierFileUploaderView.as_view()),
    path('shippingupload/', ShippingFileUploaderView.as_view()),
    path('semesterresultupload/', SemesterResultsFileUploaderView.as_view()),
    #path('email-template/', views.my_email_template_view, name='email-template'),
    path('accountverification/<str:id>/', AccountActivationView.as_view()),
    
    #Saving URL
    path('schoolsetup/', SaveSchoolSettingView.as_view()),
    path('school/', SchoolSettingsView.as_view()),
    path('savefaculty/',    SaveFacultyView.as_view()),
    path('savefaculty/<str:id>/',    SaveFacultyView.as_view()),
    path('savedepartment/',    SaveDepartmentView.as_view()),
    path('savedepartment/<str:id>/',    ListDepartmentView.as_view()),
    path('savedepartment/departmentlist/<str:id>/<str:fac>/',    SaveDepartmentView.as_view()),
    path('saveprogramme/',    SaveProgrammeView.as_view()),
    path('saveprogramme/<str:id>/',    ListProgrammeView.as_view()),
    path('saveprogramme/<str:id>/<str:dept>/',    SaveProgrammeView.as_view()),
    path('savesemester/',    SaveSemesterView.as_view()),
    path('savesemester/<int:session>/<str:id>',    SaveSemesterView.as_view()),
    path('savestudentrecords/',    SaveStudentRecordsView.as_view()),
    path('savescourses/',    SaveCoursesView.as_view()),
    path('savescourses/<str:id>', SaveCoursesView.as_view()),
    path('savesession/',    SaveSessionView.as_view()),
    path('savesession/<str:id>',    SaveSessionView.as_view()),
    path('savecourier/',    SaveCourierView.as_view()),
    path('savecourier/<str:id>/',    SaveCourierView.as_view()),
    path('saveshipping/',    SaveShippingView.as_view()),
    path('savegrade/',    SaveGradeView.as_view()),
    path('savegrade/<str:id>/',    SaveGradeView.as_view()),
    path('savelevel/',    SaveLevelView.as_view()),
    path('savelevel/<str:id>',    ListLevelView.as_view()),
    path('savelevel/<int:session>/<str:id>',    SaveLevelView.as_view()),
    path('savecountry/',    SaveCountryView.as_view()),
    path('savecountry/<int:id>',    SaveCountryView.as_view()),
    path('savestate/',    SaveStateView.as_view()),
    path('savestate/<int:cid>',    SaveStateView.as_view()),
    path('studentresults/', SaveResultOfStudentsView.as_view()),
    path('searchstudentrecords/',GetStudentInformationList.as_view()),
    path('saveroles/', SaveRolesView.as_view()),
    path('saveroles/<str:id>/', SaveRolesView.as_view()),
    path('saveuserrole/', SaveUsersRoleView.as_view()),
    path('saveuserrole/<str:id>/', SaveUsersRoleView.as_view()),
    path('getuserrole/<str:id>/', ListUserRolesView.as_view()),
    path('studentresult/', SaveResultOfStudentsView.as_view()),
    path('fetchschools/', ListSchoolAccountView.as_view()),
    path('fetchschoolsbyid/<str:id>', ListSchoolAccountView.as_view()),
    path('activateschools/', ActivateSchoolView.as_view()),
    
    path('savecurriculum/', SaveCurriculumView.as_view()),
    path('getstudentcourses/', GetStudentCoursesView.as_view()),
    path('savegraduationyear/', SaveGraduationYearView.as_view()),
    path('savegraduationyear/<str:id>', SaveGraduationYearView.as_view()),
    path('savedegreeclass/', SaveDegreeclassView.as_view()),
    path('savedegreeclass/<str:id>', SaveDegreeclassView.as_view()),
    path('savesemesterresult/', SaveSemesterResultView.as_view()),
    path('savepermission/', SavePermissionsView.as_view()),
    path('savepermission/<str:id>', SavePermissionsView.as_view()),
    path('saverolepermission/', SaveRolePermissionView.as_view()),
    path('saverolepermission/<str:id>', SaveRolePermissionView.as_view()),
    path('changelogo/', SaveChangeLogoView.as_view()),
    path('getstudent/', GetStudentInformationLists.as_view()),
    path('getstudentsessions/', GetStudentSessionsView.as_view()),
    path('getresultsofstudent/', GetStudentSessionsView.as_view()),
    #Generate Transcript
    path('generatetranscript/', GenerateTranscriptView.as_view()),
    path('getresultofstudent/',   GetStudentResultsView.as_view()),
    #update path
    path('levelupdate/',   LevelUpdateView.as_view()),
    path('departmentupdate/',   DepartmentUpdateView.as_view()),
    path('programmeupdate/',   ProgrammeUpdateView.as_view()),
    path('sessionupdate/',   SessionUpdateView.as_view()),
    #Delete path
    path('deleteuser/<int:id>/', DeleteUsersView.as_view()),
    path('deletefaculty/<int:id>/', DeleteFacultyView.as_view()),
    path('deletelevel/<int:id>/', DeleteLevelView.as_view()),
    path('deletedepartment/<int:id>/', DeleteDepartmentView.as_view()),
    path('deleteprogramme/<int:id>/', DeleteProgrammeView.as_view()),
    path('deletesession/<int:id>/', DeleteSessionView.as_view()),
    
    
    path('logout/', LogoutView.as_view()),
    path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    #path('verify_email/<int:pk>/', verify_email, name='verify_email'),
    path('openapi/', get_schema_view(
        title="School Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
]