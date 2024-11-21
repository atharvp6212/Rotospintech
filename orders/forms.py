from django import forms
from .models import Order, OrderedSubPart
from inventory.models import SubPart, Color

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # Use default fields, or specify fields as needed

class OrderedSubPartForm(forms.ModelForm):
    color = forms.ModelChoiceField(queryset=Color.objects.none(), required=True)

    class Meta:
        model = OrderedSubPart
        fields = ['sub_part', 'quantity', 'color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially set color queryset to none
        self.fields['color'].queryset = Color.objects.none()
        
class OrderedSubPartFormSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.none()  # Disable queryset

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['sub_part'] = forms.ModelChoiceField(
            queryset=SubPart.objects.all(),
            label=f"Sub-Part {index + 1}"
        )
        form.fields['quantity'] = forms.IntegerField(
            min_value=1,
            label=f"Quantity {index + 1}"
        )

    def clean(self):
        super().clean()
        # Optionally, you can add custom validation here
