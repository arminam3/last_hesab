from django import forms

from .models import Week, Shopping, Money


# class MoneyForm(forms.Form):
    # class Meta:
    #     fields = ['user',
    #     model = Money'week', 'money']

    # user = forms.Select()
    # week = forms.Select()
    # money = forms.IntegerField()

class CreateMoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['user']

class CreateShoppingForm(forms.ModelForm):
    class Meta:
        model = Shopping
        fields = ['name', 'buyer', 'consumer', 'amount', 'goods']
        widgets = {
            'day'
        }


