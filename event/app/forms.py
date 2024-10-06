from django import forms
from .models import Vendor_Registration,Product,User_Registration

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor_Registration
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")  # Fixed typo here
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'photo', 'description']
        
class UserForm(forms.ModelForm):
    class Meta:
        model=User_Registration
        fields = ['username', 'email', 'password', 'confirm_password','Address']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
            'Address':forms.Textarea(attrs={
                'cols':40,
                'rows':3,
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")  # Fixed typo here
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor_Registration
        fields = ['username', 'email']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User_Registration
        fields = ['username', 'email','Address']