from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from typing import cast, Dict, Any
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Users, UserManager, EmailVerify
from django_ratelimit.decorators import ratelimit
from . import template, send_email
import secrets
from django.utils import timezone
from datetime import timedelta


EXPIRE = 60*60*24  # Email Verification allows till 24 hour

# Check email if in correct format
def is_valid_email(email: str) -> bool:
  try:
    validate_email(email)
    return True
  except ValidationError:
    return False

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

  if not is_valid_email(cast(str, email)):
    return Response(
      {
        "result": False,
        "reason": "invalid email address"
      }, status=status.HTTP_400_BAD_REQUEST
    )
  
  user = authenticate(request._request, email=email, password=password)
  
  if user is not None and user.is_active:
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
  
  if not is_valid_email(cast(str, email)):
    return Response(
      {
        "result": False,
        "reason": "invalid email address"
      }, status=status.HTTP_400_BAD_REQUEST
    )

  try:
    manager = cast(UserManager, Users.objects)
    user = manager.create_user(email=cast(str, email), password=password, firstname=firstname, lastname=lastname)
    
    token = secrets.token_urlsafe(32)
    EmailVerify.objects.create(id=user, token=token)

    body = template.load_email_verify(f"http://localhost:5173/verify-email?token={token}", EXPIRE)

    if send_email.EMAIL is None:
      return Response(
        {
          "result": False,
          "reason": "email server is not ready"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    
    email_sent = send_email.EMAIL.send(
      to=cast(str, email),
      subject="Verify your email",
      html_body=body
    )

    if not email_sent:
      return Response(
        {
          "result": False,
          "reason": "unable to send email"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

    return Response(
      {
        "result": True,
        "description": "email send successfully"
      }, status=status.HTTP_200_OK
    )
  except Exception:
    return Response(
      {
        "result": False,
        "reason": "email already exist or server error"
      }, status=status.HTTP_400_BAD_REQUEST
    )

@ratelimit(key="ip", rate="2/m", block=True)
@api_view(["POST"])
def verify_email(request: Request):
  data = cast(Dict[str, str], request.data)
  token = data.get("token")
  if token is None:
    return Response(
      {
        "result": False,
        "reason": "token is required"
      }, status=status.HTTP_400_BAD_REQUEST
    )

  # Check if email exist
  try:
    verification_token = EmailVerify.objects.get(token=token)
    user = verification_token.id

    if verification_token.created_at < (timezone.now() - timedelta(seconds=EXPIRE)):
      verification_token.delete()
      user.delete()
      return Response(
        {
          "result": False,
          "reason": "the link has expired"
        }, status=status.HTTP_410_GONE
      )

    user.is_active = True
    user.save()
    verification_token.delete()
    return Response(
      {
        "result": True,
        "description": "user registered successfully"
      }, status=status.HTTP_201_CREATED
    )
  except EmailVerify.DoesNotExist:
    return Response(
      {
        "result": False,
        "reason": "invalid token or the email doesn't exist"
      }, status=status.HTTP_404_NOT_FOUND
    )
