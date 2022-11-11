from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLessSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework import exceptions

from mainproject.iroha_config import *

class WhoAmI(APIView):
    permission_classes = [IsAuthenticated]
    """
    Gives the current authenticated user
    """

    def get(self, request):
        user = request.user
        serializer = UserLessSerializer(request.user)
        return Response(serializer.data)


class RegisterUser(APIView):
    serializer_class = UserLessSerializer
    available_role = ["Customer", "Enterprise"]

    def post(self, request):
        data = request.data
        if data.get("password") != data.get("password_confirm"):
            raise exceptions.APIException("Password doesn't match !")
        if User.objects.filter(email=data.get("email")).exists():
            raise exceptions.APIException("Email already taken !")
        if User.objects.filter(username=data.get("username")).exists():
            raise exceptions.APIException("Username already taken !")
        role = data.get("role")
        if role:
            if role not in self.available_role:
                raise exceptions.APIException("Incorrect Role !")
        try:
            user = User.objects.create_user(
                email=data.get("email"),
                username=data.get("username"),
                password=data.get("password"),
                role= data.get('role','Customer')
            )
            serializer = self.serializer_class(user)
            return Response(
                {"detail": "Successfully registered", "data": serializer.data}
            )
        except Exception as e:
            return Response({"detail": str(e)})
