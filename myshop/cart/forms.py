from django import forms

PRODUCT_QANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices= PRODUCT_QANTITY_CHOICES )
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
