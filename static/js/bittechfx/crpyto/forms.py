#forms.py
from django import forms  
from crpyto.models import Deposit_history, Userwallet, UserMembership
from django.forms import ModelForm

class EmployeeForm(ModelForm):  
    class Meta:
        model = Deposit_history  
        fields = ['currency','status']#https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
     

class OrderForm(ModelForm):
    class Meta:
        model = Userwallet
        fields = ['deposited','profit','bonus','ref_bonus']


class MembershipForm(ModelForm):
    class Meta:
        model = UserMembership
        fields = ['membership','amount']
        widgets = {
            'membership':forms.Select(attrs={'class':'btn-group bootstrap-select btn dropdown-toggle btn-default'}),
            'amount':forms.TextInput(attrs={'class':'bootstrap-select btn vertical-spin form-control','placeholder':'Your amount ....','data-bts-button-down-class':'btn btn-secondary', 'data-bts-button-up-class':'btn btn-secondary'})
        }
    # def __init__(self, *args, **kwargs):
    #     super(MembershipForm, self).__init__(*args, **kwargs)
    #     self.fields['membership'].label = ""
    #     self.fields['amount'].label = ""