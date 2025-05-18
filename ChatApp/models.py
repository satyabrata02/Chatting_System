from django.db import models

# Create your models here.

class Userreg(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    phoneno = models.BigIntegerField(primary_key=True, unique=True)
    emailid = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    secure_question = models.CharField(max_length=50)
    answer = models.CharField(max_length=45)
    status = models.CharField(max_length=15, default='offline')
    images = models.CharField(max_length=50, default='user.png')
    is_set_auth = models.BooleanField(default=False)
    auth_token = models.TextField(blank=True, null=True)

class Systemchat(models.Model):
    chatid = models.AutoField(primary_key=True)
    fromuser = models.CharField(max_length=15)
    touser = models.CharField(max_length=15)
    message = models.CharField(max_length=500)
    chat_date = models.CharField(max_length=50)

class Contactus(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phoneno = models.BigIntegerField()
    emailid = models.EmailField()
    message = models.TextField()
