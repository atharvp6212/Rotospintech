from django import forms
from .models import Product, SubPart, RawMaterial, SubPartRawMaterial

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ['name', 'quantity']

class SubPartForm(forms.ModelForm):
    class Meta:
        model = SubPart
        fields = ['name']

class ProductForm(forms.ModelForm):
    num_sub_parts = forms.IntegerField(min_value=1, label="Number of Sub-Parts")

    class Meta:
        model = Product
        fields = ['name']

    def __init__(self, *args, **kwargs):
        num_sub_parts = kwargs.pop('num_sub_parts', None)
        super(ProductForm, self).__init__(*args, **kwargs)

class SubPartRawMaterialForm(forms.ModelForm):
    class Meta:
        model = SubPartRawMaterial
        fields = ['raw_material', 'quantity_required']

    def __init__(self, *args, **kwargs):
        super(SubPartRawMaterialForm, self).__init__(*args, **kwargs)
        self.fields['raw_material'].queryset = RawMaterial.objects.all()
        self.fields['quantity_required'].widget = forms.NumberInput(attrs={'min': 0.1})

class SubPartFormSet(forms.BaseFormSet):
    def add_fields(self, form, index):
        super(SubPartFormSet, self).add_fields(form, index)
        form.fields['sub_part_name'] = forms.CharField(
            label=f'Sub-Part Name {index+1}', max_length=100
        )
        form.fields['quantity_required'] = forms.FloatField(
            label=f'Quantity Required for Sub-Part {index+1}', min_value=0.1
        )

class RawMaterialFormSet(forms.BaseFormSet):
    def add_fields(self, form, index):
        super(RawMaterialFormSet, self).add_fields(form, index)
        form.fields['raw_material'] = forms.ModelChoiceField(
            queryset=RawMaterial.objects.all(), label=f'Raw Material {index+1}'
        )
        form.fields['quantity_required'] = forms.FloatField(
            label=f'Quantity Required {index+1}', min_value=0.1
        )

# New form to handle entering stock for existing raw materials
class EnterStockForm(forms.Form):
    raw_material = forms.ModelChoiceField(queryset=RawMaterial.objects.all(), label="Select Raw Material")
    quantity_received = forms.FloatField(min_value=0.1, label="Quantity Received")
