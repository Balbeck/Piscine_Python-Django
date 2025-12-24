from django import forms

class LogForm(forms.Form):
    """Formulaire pour saisir une entrée de log"""
    text = forms.CharField(
        label='Log Entry',
        max_length=500,
        widget=forms.TextInput(attrs={
            'placeholder': 'inputs...',
            'class': 'form-input'
        })
    )
