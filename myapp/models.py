from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class expert_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.BigIntegerField()
    place=models.CharField(max_length=300)
    pincode=models.IntegerField()
    district=models.CharField(max_length=200)
    photo=models.FileField()

class user_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    place = models.CharField(max_length=300)
    pincode = models.IntegerField()
    district = models.CharField(max_length=200)
    photo = models.FileField()

class company_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.BigIntegerField()
    sinceyear=models.IntegerField()
    proof=models.FileField()
    photo=models.FileField()
    place=models.CharField(max_length=300)
    pincode=models.IntegerField()
    state=models.CharField(max_length=300)
    district=models.CharField(max_length=200)
    latitude=models.FloatField()
    longtitude=models.FloatField()
    status= models.CharField(max_length=300)

class feedback(models.Model):
    date=models.DateField()
    feedback= models.CharField(max_length=300)
    rating=models.FloatField()
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class company_review(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=300)
    rating=models.FloatField()
    COMPANY=models.ForeignKey(company_table,on_delete=models.CASCADE)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=300)
    reply=models.CharField(max_length=300)
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)

class stock_table(models.Model):
    name=models.CharField(max_length=100)
    photo=models.FileField()
    price=models.FloatField()
    details=models.CharField(max_length=300)
    COMPANY=models.ForeignKey(company_table,on_delete=models.CASCADE)

class StockDailyHistory(models.Model):
    STOCK=models.ForeignKey(stock_table,on_delete=models.CASCADE)
    starting=models.FloatField()
    ending=models.FloatField()
    date=models.DateField()


class tips(models.Model):
    date=models.DateField()
    tiptitle=models.CharField(max_length=200)
    description=models.CharField(max_length=300)
    EXPERT=models.ForeignKey(expert_table,on_delete=models.CASCADE)

class doubt(models.Model):
    date=models.DateField()
    doubt=models.CharField(max_length=300)
    reply = models.CharField(max_length=300)
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    EXPERT=models.ForeignKey(expert_table,on_delete=models.CASCADE)


class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)







