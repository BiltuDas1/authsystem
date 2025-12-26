from . import models, serializers
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from typing import cast, Any, Dict
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users

# Create your views here.
@api_view(['POST'])
def login(request: Request):
  data = cast(Dict[str, Any], request.data)

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
  return Response()