from django.urls import path, include
from .views import *
urlpatterns = [
    path("company-list/", WasteCompanyList.as_view()),
    path("company-user/", CompanyCustomerList.as_view()),

]

