from django.contrib import admin
from ChatApp.models import Userreg, Systemchat, Contactus

# Register your models here.

class UserregAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'gender', 'phoneno', 'emailid', 'password', 'secure_question', 'answer', 'status', 'images']

class SystemchatAdmin(admin.ModelAdmin):
    list_display = ['chatid', 'fromuser', 'touser', 'message', 'chat_date']

class ContactusAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'phoneno', 'emailid', 'message']

admin.site.register(Userreg, UserregAdmin)
admin.site.register(Systemchat, SystemchatAdmin)
admin.site.register(Contactus, ContactusAdmin)
