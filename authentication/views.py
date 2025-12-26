from . import models, serializers
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from typing import cast, Dict
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users, UserManager

# Create your views here.
@api_view(['POST'])
def login(request: Request):
  data = cast(Dict[str, str], request.data)

  email = data.get("email")
  password = data.get("password")

  if not email or not password:
    return Response(
      {
        'result': False,
        'reason': 'Please provide both email and password'
      }, status=status.HTTP_400_BAD_REQUEST
    )
  
  user = authenticate(request._request, email=email, password=password)
  
  if user is not None:
    user = cast(Users, user)

    refresh_token = RefreshToken.for_user(user)

    return Response(
      {
        'result': True,
        'access_token': str(refresh_token.access_token),
        'refresh_token': str(refresh_token),
        'user': {
          'id': user.id,
          'firstname': user.firstname,
          'lastname': user.lastname,
          'email': user.email,
          'role': user.role
        }
      }, status=status.HTTP_200_OK
    )
  return Response(
    {
      'result': False,
      'reason': 'invalid email or password'
    }, status=status.HTTP_400_BAD_REQUEST
  )

@api_view(['POST'])
def register(request: Request):
  data = cast(Dict[str, str], request.data)

  firstname = data.get("firstname")
  lastname = data.get("lastname")
  email = data.get("email")
  password = data.get("password")

  required_fields = ("firstname", "lastname", "email", "password")
  for field in required_fields:
    if not data.get(field):
      return Response(
        {
          "result": False, 
          "reason": f"{field} is required"
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
  manager = cast(UserManager, Users.objects)
  try:
    manager.create_user(email=cast(str, email), password=password, firstname=firstname, lastname=lastname)

    return Response(
      {
        "result": True,
        "description": "user registered successfully"
      }, status=status.HTTP_201_CREATED
    )
  except Exception:
    return Response(
      {
        "result": False,
        "reason": "email already exist or server error"
      }, status=status.HTTP_400_BAD_REQUEST
    )