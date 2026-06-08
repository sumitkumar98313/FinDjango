from django import forms
from .models import Transaction, Profile


# form for adding a new transaction
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'description', 'amount', 'category', 'date']

        # adding css class and placeholder to each field
        widgets = {
            'type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Salary, Groceries...'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'min': '0'
            }),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }


# form for editing user profile - picture and budget
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'monthly_budget']

        widgets = {
            'monthly_budget': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'min': '0'
            }),
        }
