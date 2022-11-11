from django.db import models
from users.models import User
# Create your models here.


class WasteManagementCompany(models.Model):
    name = models.CharField(max_length=200,unique=True)
    detail = models.TextField(blank=True,default='')
    avatar = models.ImageField(default='default.jpg', upload_to='company')
    monthly_fee = models.IntegerField()
    owner = models.OneToOneField("users.User", on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.name




class PickUpHistory(models.Model):
    '''
        Tracks the pick up 
        For eg : Picked up trash on 23rd october for Rayon 
    '''
    company = models.ForeignKey(WasteManagementCompany, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    trash_weight = models.FloatField()
    rewarded = models.BooleanField(default=False)
    is_segregated = models.BooleanField(default=True)
    date_created = models.DateTimeField( auto_now_add=True)




class CompanyCustomer(models.Model):
    '''
        Track Customer of COmpany
        this model can be used by both company and users to track the subscription
        User can see their old subscribed waste cmpany
        Company can see their customers
    '''
    company = models.ForeignKey(WasteManagementCompany, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_date = models.DateField( auto_now=False, auto_now_add=False)
    is_still_a_customer = models.BooleanField() #if false then customer lost 





