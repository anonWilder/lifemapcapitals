from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
		'class': 'form-control ps-15 bg-transparent',
		'placeholder': 'Email.......',

	}))
	# mob = forms.IntegerField() # newly added

	class Meta:
		model = User
		fields = ('first_name','last_name','username', 'email')
		widgets = {
			'first_name':forms.TextInput(attrs={'class':'','placeholder':'First Name'}),
			'last_name':forms.TextInput(attrs={'class':'','placeholder':'Last Name'}),
			'username':forms.TextInput(attrs={'class':'','placeholder':'username'}),
			'email':forms.TextInput(attrs={'class':'','placeholder':'Email'}),
			
		}

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['email'].label = ""
	# 	self.fields['username'].label = ""

