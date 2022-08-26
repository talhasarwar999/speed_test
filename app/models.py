from django.db import models

# Create your models here.

class Contact(models.Model):
    name      = models.CharField(max_length=100)
    email     = models.EmailField(max_length=100)
    phone     = models.IntegerField()
    message   = models.TextField()
    con_date  = models.DateField(auto_now_add=True)
    def __str__(self):
       return  "Name : " + self.name + " --- Email : " + self.email


class Subscribe(models.Model):
    email             = models.EmailField(max_length=100)
    subscription_date = models.DateField(auto_now_add=True)
    def __str__(self):
       return  "Email : " + self.email


