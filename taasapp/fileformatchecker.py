import csv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import io  # Add this import
from io import TextIOWrapper
def is_valid_csv(file):
   try:
        if not file.name.endswith('.csv'):
            return False
        return True
   except (csv.Error, UnicodeDecodeError):
        return False
