from django.db import models

# Create your models here. janu ho gaya baby user dubara
class station(models.Model):
    city=models.CharField(max_length=20,default=None,null=True)
    country=models.CharField(max_length=20,default=None,null=True)
    statecode=models.CharField(max_length=6,default=None,null=True)
    lat=models.CharField(max_length=15,default=None,null=True)
    long=models.CharField(max_length=15,default=None,null=True)
    ts=models.DateTimeField(auto_now_add=True)
    uts=models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ("city", "statecode","country")