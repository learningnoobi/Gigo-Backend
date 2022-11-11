from django.urls import path, include
from .views import (
    WhoAmI, RegisterUser, GetAccountAsset,MyTokenObtainPairView,TransferTrashCoin,GetAccountTransactions
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("whoami/", WhoAmI.as_view()),
    path("register/", RegisterUser.as_view()),
    path("get-account-asset/", GetAccountAsset.as_view()),
    path("transfer-coin/", TransferTrashCoin.as_view()),
    path("account-transactions/", GetAccountTransactions.as_view()),
    # path("get-my-qrcode/", GetMyQRCodeDetail.as_view()),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

