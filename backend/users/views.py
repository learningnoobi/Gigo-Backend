from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLessSerializer,MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from rest_framework import exceptions
from .utils import create_iroha_account, get_asset_of_user
from mainproject.iroha_config import *
from django.db import transaction
from google.protobuf.json_format import MessageToJson,MessageToDict
from rest_framework import renderers
import io
import segno
from django.core.files.base import ContentFile
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import send_transaction_and_print_status

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
            iroha_name = f'{data.get("username")}@gigo'
            user.iroha_name = iroha_name
            out = io.BytesIO()
            qr = segno.make(iroha_name, micro=False)
            qr.save(out, kind='png', dark='#000000', light=None, scale=3)
            filename = 'qr-'+user.username+'.png'
            user.qr_code.save(filename, ContentFile(out.getvalue()), save=False)
            user.save()
            return Response(
                {
                    "detail": "Successfully registered",
                    "data": serializer.data,
                    "private_key": private_key,
                }
            )
        except Exception as e:
            print(e)
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
            print(user.iroha_name)
            asset_detail = get_asset_of_user(user.iroha_name)
            print('asset_detail : ',asset_detail)

            serialized = MessageToDict(asset_detail)['accountAssets']
            print('serialized ',asset_detail)
            return Response({'data':serialized})
        except Exception as e:
            print(e)
            raise exceptions.APIException(str(e))




class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class TransferTrashCoin(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        data = request.data
        to_user_name = data.get('iroha_name')
        if not User.objects.filter(iroha_name = to_user_name).exists():
            raise exceptions.APIException("No account found with given iroha name !")
        to_user =  User.objects.filter(iroha_name = to_user_name).first()
        iroha_user = Iroha(user.iroha_name)
        tx = iroha_user.transaction(
        [iroha_user.command(
            'TransferAsset', src_account_id=user.iroha_name, dest_account_id=to_user_name,
            asset_id='trashcoin#gigo', amount='1'
        )])
        IrohaCrypto.sign_transaction(tx, data.get('private_key'))
        send_transaction_and_print_status(tx)
        return Response({"detail":f"Sent coin to {to_user.username}"})
        



# class GetAccountTransactions(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         data = request.data
#         private_key = data.get('private_key')
#         if not private_key:
#             raise exceptions.APIException("Private key needed !")
#         try:
#             asset_detail = get_asset_of_user(user.iroha_name,private_key)
#             serialized = MessageToDict(asset_detail)['accountAssets']
#             return Response({'data':serialized})
#         except Exception as e:
#             raise exceptions.APIException(str(e))






# from django.core.files.base import ContentFile

# class GetMyQRCodeDetail(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self,request):  
#         user = request.user
#         #qr code
#         out = io.BytesIO()
#         qr = segno.make(user.iroha_name, micro=False)
#         qr.save(out, kind='png', dark='#000000', light=None, scale=3)
#         filename = 'qr-'+user.username+'.png'
#         user.qr_code.save(filename, ContentFile(out.getvalue()), save=False)
#         user.save()
#         return Response({'selected':'b'})