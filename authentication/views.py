from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from typing import cast, Dict, Any
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Users, UserManager
from django_ratelimit.decorators import ratelimit

# Create your views here.
@ratelimit(key="ip", rate="5/m", block=True)
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
def logout(request: Request):
  data = cast(Dict[str, str], request.data)
  refresh_token = data.get("refresh_token")
  if refresh_token is None:
    return Response(
      {
        "result": False,
        "reason": "no refresh_token provided"
      }, status=status.HTTP_400_BAD_REQUEST
    )

  try:
    token = RefreshToken(cast(Any, refresh_token))
    token.blacklist()
    return Response(
      {
        "result": True,
        "description": "logout successful"
      }, status=status.HTTP_202_ACCEPTED
    )
  except TokenError:
    return Response(
      {
        "result": False,
        "reason": "invalid refresh_token"
      }, status=status.HTTP_400_BAD_REQUEST
    )
  
@ratelimit(key="ip", rate="5/m", block=True)
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