from ..models import Roles, RolePermissions, Permissions
from ..serializers import SaveRolePermissionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from rest_framework.exceptions import APIException
import sys
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

class SaveRolePermissionView(APIView):
    serializer_class =SaveRolePermissionSerializer
    permission_classes = []
    @swagger_auto_schema(request_body=SaveRolePermissionSerializer)
    
    def post(self, request):
        if request.method == 'POST':
            serializer = SaveRolePermissionSerializer(data=request.data)
        try:
            if serializer.is_valid():
          
              
                role_check = Roles.objects.filter(id = request.data['roleID'])
                if not role_check:
                    return Response({"error":"Role not  exists","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
                
                permission_check = Permissions.objects.filter(id = request.data['permissionID'])
                if not permission_check:
                    return Response({"error":"Permission not  exists","statuscode":404, 'message':'NOT_FOUND', },status=status.HTTP_404_NOT_FOUND)
               
                rolepermission_check = RolePermissions.objects.filter(permissionID = request.data['permissionID']).filter(roleID = request.data['roleID']).filter(userID = request.data["userID"])
                if rolepermission_check:
                    return Response({"error":"Role Permission already exists","statuscode":208, 'message':'ALREADY_EXIST', },status=status.HTTP_208_ALREADY_REPORTED)

                serializer.save()
                rolesPermissionCount = RolePermissions.objects.filter(userID = request.data["userID"]).count()
            
                return Response({
                                 'userID':request.data['userID'],
                                 'affectedRows':rolesPermissionCount, 
                                 'expireDate':datetime.datetime.now(),
                                 'message':'SAVED_SUCCESS',
                                 'statuscode':200,
                                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
       
        return Response({'message':'SERVER_ERORR','error':serializer.errors}) 
    
    def get(self,request, id=None):
         if request.method == 'GET':
             try:       
                    rolesPermission = RolePermissions.objects.filter(userID =id)
                    serializer = SaveRolePermissionSerializer( rolesPermission, many=True)
                    return Response({'message':'FETCH_SUCCESS','data':serializer.data}) 
             except Exception as e:
                    return Response({'message':'SERVER_ERORR','error':repr(e), 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
              
         return Response({'message':'SERVER_ERORR','error':"Server Error", 'expireDate':datetime.datetime.now(), 'statuscode':'500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
  
        