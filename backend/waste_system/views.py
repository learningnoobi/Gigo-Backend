from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions,generics,filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import WasteCompanySerializer,CompanyCustomerSerializers
from django_filters.rest_framework import DjangoFilterBackend


class WasteCompanyList(generics.ListAPIView):
    queryset = WasteManagementCompany.objects.all()
    serializer_class = WasteCompanySerializer
    search_fields = ['name']
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset()
      

class CompanyCustomerList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CompanyCustomer.objects.all()
    serializer_class = CompanyCustomerSerializers
    search_fields = ['customer__username']
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        company = WasteManagementCompany.objects.filter(owner = user).first()
        tracks =company.companycustomer_set.filter(is_still_a_customer=True)
        return tracks