
from .models import Department, Faculty, Programme, Session

def check_faculty_existence(request):
       facultycode = request.data.get('facultycode')
       userid = request.data.get('userID')
       existing_faculty = Faculty.objects.filter(facultycode=facultycode, userID=userid)
       if existing_faculty.exists():
            return True
       return False
    
def check_department_existence(request):
    department_code = request.data.get('departmentcode')
    user_id = request.data.get('userID')
    existing_department = Department.objects.filter(departmentcode=department_code, userID=user_id)
    if existing_department.exists():
        return True
    return False
    
def check_programme_existence(request):
    programmecode = request.data.get('programmecode')
    user_id = request.data.get('userID')
    existing_programme = Programme.objects.filter(programmecode=programmecode, userID=user_id)
    if existing_programme.exists():
        return True
    return False

def check_session_existence(request):
    session = request.data.get('name')
    user_id = request.data.get('userID')
    existing_session = Session.objects.filter(name=session, userID=user_id)
    if existing_session.exists():
        return True
    return False
# You can then call this function wherever needed in your code
