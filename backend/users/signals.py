from django.dispatch import receiver    
from django.db.models.signals import post_save
from django.core.files.base import ContentFile

import io
import segno
from .models import User

# @receiver(post_save,sender=User)
# def user_create_signal(sender, instance,created ,*args, **kwargs):
#     if created:
#         print('signlas')
#         out = io.BytesIO()
#         qr = segno.make(instance.iroha_name, micro=False)
#         qr.save(out, kind='png', dark='#000000', light=None, scale=3)
#         filename = 'qr-'+instance.username+'.png'
#         instance.qr_code.save(filename, ContentFile(out.getvalue()), save=False)
#         instance.save()