from django.db import models
from django.contrib.auth.models import User


class Week(models.Model):
    name = models.CharField(max_length=100)
    date_create = models.DateField(auto_now_add=True)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Shopping(models.Model):
    CHOICES = (('0', 'شنبه'),
               ('1', 'یکشنبه'),
               ('2', 'دوشنبه'),
               ('3', 'سه شنبه'),
               ('4', 'چهارشنبه'),
               ('5', 'پنج شنبه'),
               ('6', 'جمعه')
               )

    name = models.CharField(choices=CHOICES, max_length=100)
    week = models.ForeignKey(Week, on_delete=models.PROTECT, related_name='weekshopping', null=True)
    day = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usershopping')
    consumer = models.ManyToManyField(User)
    amount = models.IntegerField()
    goods = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.day} | {self.buyer}'


class Money(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermoney')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='weekmoney')
    money = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} | {self.week} | {0 if self.money==0 else self.money}'

class Hesab(models.Model):
    plus = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userhesab_p')
    negative = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userhesab_n')
    amount = models.IntegerField()
    week = models.ForeignKey(Week, on_delete=models.PROTECT, related_name='weekhesab', null=True)

    def __str__(self):
        return f'{self.negative.username} ==> {self.plus.username}'


class MainHesab(models.Model):
    plus = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermainhesab_p')
    negative = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermainhesab_n')
    amount = models.IntegerField(null=True)
    week = models.ForeignKey(Week, on_delete=models.PROTECT, related_name='weekmainhesab', null=True)

    def __str__(self):
        return f'{self.negative.username} ==> {self.plus.username}'


class LastHesab(models.Model):
    plus = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlasthesab_p')
    negative = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlasthesab_n')
    amount = models.IntegerField(null=True)
    week = models.ForeignKey(Week, on_delete=models.PROTECT, related_name='weeklasthesab', null=True)
