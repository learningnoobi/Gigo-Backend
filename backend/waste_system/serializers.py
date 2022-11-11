from rest_framework import serializers
from .models import *
from users.serializers import UserLessSerializer

class WasteCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = WasteManagementCompany
        fields = "__all__"


class CompanyCustomerSerializers(serializers.ModelSerializer):
    customer = UserLessSerializer()

    class Meta:
        model = CompanyCustomer
        fields = "__all__"


