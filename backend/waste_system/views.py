from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions,generics,filters,status
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

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
        print('user is ',user)
        company = WasteManagementCompany.objects.filter(owner = user).first()
        if not company:
            raise exceptions.APIException("No Company Yet !")
        tracks =company.companycustomer_set.filter(is_still_a_customer=True)
        return tracks

class SubscribeToCompany(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data
        user = request.user
        company_id = data.get('company_id')
        company = get_object_or_404(WasteManagementCompany,id=company_id)
        user.subscribed_company = company
        user.save()
        CompanyCustomer.objects.filter(customer=user).update(is_still_a_customer=False)
        CompanyCustomer.objects.create(company=company,customer=user,is_still_a_customer=True)
        return Response({'detail':f'Successfully Subscribed to {company.name}.'})

class RemoveSubscribeOfCompany(APIView):
    def post(self,request):
        data = request.data
        user = request.user
        company_id = data.get('company_id')
        company = get_object_or_404(WasteManagementCompany,id=company_id)
        user.subscribed_company = None
        user.save()
        CompanyCustomer.objects.filter(customer=user).update(is_still_a_customer=False)
        return Response({'detail':f'Successfully Unsubscribed to {company.name}.'})

class MySubscribedCompany(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        print('user is ',user)
        if not user.subscribed_company:
            return Response({"detail":"Not Subscribed to any company yet!"},status = status.HTTP_404_NOT_FOUND)
        serializer = WasteCompanySerializer(user.subscribed_company,context={'request':request})
        return Response(serializer.data)

