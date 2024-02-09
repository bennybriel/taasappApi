from rest_framework.response import Response
from rest_framework import status
from .models import Users, Apikeys  # Replace with the actual import for your Users model

def authenticate_user(request, id):
    # Get the 'Authorization-Key' from the request headers
    auth_key = request.headers.get('Authorization-Key')
    
    # Check if the 'Authorization-Key' is present
    if not auth_key:
        return False, Response({'message': 'NOT_FOUND', 'error': 'No Api Key Supplied', 'statuscode': '404'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the user based on the provided 'id'
    user = Apikeys.objects.filter(userID=id).first()

    # Check if the user exists
    if not user:
        return False, Response({'message': 'NOT_FOUND', 'error': 'User not found', 'statuscode': '404'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has an associated API key
    api_key = getattr(user, 'apikey', None)

    if not api_key:
        return False, Response({'message': 'NOT_FOUND', 'error': 'User does not have an API key', 'statuscode': '404'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the provided 'Authorization-Key' matches the user's API key
    if auth_key != api_key:
        return False, Response({'message': 'NOT_FOUND', 'error': 'Invalid Api Key Supplied', 'statuscode': '404'}, status=status.HTTP_404_NOT_FOUND)

    # Authentication successful
    return True, None
