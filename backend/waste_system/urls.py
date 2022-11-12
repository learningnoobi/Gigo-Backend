from django.urls import path, include
from .views import *
urlpatterns = [
    path("company-list/", WasteCompanyList.as_view()),
    path("company-user/", CompanyCustomerList.as_view()),
    path("my-subscribed-company/", MySubscribedCompany.as_view()),
    path("subscribe-company/", SubscribeToCompany.as_view()),
    path("unsubscribe-company/", RemoveSubscribeOfCompany.as_view()),

]

