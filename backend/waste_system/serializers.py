from rest_framework import serializers
from .models import *
from users.serializers import UserLessSerializer

class WasteCompanySerializer(serializers.ModelSerializer):
    have_i_subscribed = serializers.SerializerMethodField()


    class Meta:
        model = WasteManagementCompany
        fields = "__all__"
    
    def get_have_i_subscribed(self,obj):
        request =self.context.get('request')
        user = request.user

        if not user.is_authenticated:
            return False
        return obj == user.subscribed_company


class CompanyCustomerSerializers(serializers.ModelSerializer):
    customer = UserLessSerializer()

    class Meta:
        model = CompanyCustomer
        fields = "__all__"


