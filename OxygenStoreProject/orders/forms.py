from django import forms

class OrderForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        label="Адрес",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пример: ул. Пушкина, д. 15, кв. 25'})
    )
