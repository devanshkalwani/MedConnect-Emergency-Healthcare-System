from django.contrib import admin
from .models import User, Hospital, SOSRequest

admin.site.register(User)
admin.site.register(Hospital)
admin.site.register(SOSRequest)