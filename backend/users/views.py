from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLessSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from rest_framework import exceptions
from .utils import create_iroha_account, get_asset_of_user
from mainproject.iroha_config import *
from django.db import transaction
from google.protobuf.json_format import MessageToJson,MessageToDict

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
    permission_classes = [AllowAny]

    @transaction.atomic()
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
                role=data.get("role", "Customer"),
            )
            serializer = self.serializer_class(user)
            private_key = create_iroha_account(data.get("username"))
            user.iroha_name = f'{data.get("username")}@gigo'
            user.save()
            return Response(
                {
                    "detail": "Successfully registered",
                    "data": serializer.data,
                    "private_key": private_key,
                }
            )
        except Exception as e:
            print("error")
            return Response({"detail": str(e)})

class GetAccountAsset(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        data = request.data
        private_key = data.get('private_key')
        if not private_key:
            raise exceptions.APIException("Private key needed !")
        try:
            asset_detail = get_asset_of_user(user.iroha_name,private_key)
            serialized = MessageToDict(asset_detail)['accountAssets']
            return Response({'data':serialized})
        except Exception as e:
            raise exceptions.APIException(str(e))
