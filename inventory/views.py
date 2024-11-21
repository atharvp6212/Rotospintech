from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from users.forms import WorkerCreationForm
from inventory.forms import ProductForm, SubPartRawMaterialForm, SubPartForm, RawMaterialForm, EnterStockForm
from inventory.models import Product, SubPart, SubPartRawMaterial, RawMaterial, StockHistory
from users.models import WorkerProfile

@login_required
def add_worker(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = WorkerCreationForm(request.POST)
            if form.is_valid():
                worker = form.save(commit=False)
                worker.is_worker = True
                worker.is_admin = False
                worker.save()

                # Check if a WorkerProfile already exists for this user
                if not WorkerProfile.objects.filter(user=worker).exists():
                    # Create WorkerProfile
                    WorkerProfile.objects.create(user=worker)

                return redirect('admin_dashboard')
        else:
            form = WorkerCreationForm()
        return render(request, 'inventory/add_worker.html', {'form': form})
    else:
        return render(request, 'not_authorized.html')


@login_required
def enter_stock(request):
    if request.method == 'POST':
        form = EnterStockForm(request.POST)
        if form.is_valid():
            raw_material = form.cleaned_data['raw_material']
            quantity_received = form.cleaned_data['quantity_received']
            
            # Record stock history
            quantity_before = raw_material.quantity
            quantity_after = quantity_before + quantity_received

            # Update the raw material quantity
            raw_material.quantity = quantity_after
            raw_material.save()

            # Save stock addition details in StockHistory
            StockHistory.objects.create(
                raw_material=raw_material,
                quantity_before=quantity_before,
                quantity_added=quantity_received,
                quantity_after=quantity_after
            )

            return redirect('view_raw_materials')  # Redirect to stock check page
    else:
        form = EnterStockForm()
    
    return render(request, 'inventory/enter_stock.html', {'form': form})


@login_required
def enter_order(request):
    return render(request, 'inventory/enter_order.html')

@login_required
def generate_reports(request):
    return render(request, 'inventory/generate_reports.html')

@login_required
def create_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            product_form = ProductForm(request.POST)
            num_sub_parts = request.POST.get('num_sub_parts')
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.save()
                request.session['product_id'] = product.id
                request.session['num_sub_parts'] = int(num_sub_parts)
                return redirect('define_sub_parts')
        else:
            num_sub_parts = 1  # Default value
            product_form = ProductForm(num_sub_parts=num_sub_parts)
        return render(request, 'inventory/create_product.html', {'form': product_form})
    else:
        return render(request, 'not_authorized.html')

@login_required
def define_sub_parts(request):
    num_sub_parts = request.session.get('num_sub_parts')
    product_id = request.session.get('product_id')

    if num_sub_parts:
        SubPartFormSet = forms.formset_factory(SubPartForm, extra=num_sub_parts)
        RawMaterialFormSet = forms.formset_factory(SubPartRawMaterialForm, extra=num_sub_parts)

        if request.method == 'POST':
            sub_part_formset = SubPartFormSet(request.POST, prefix='sub_parts')
            raw_material_formset = RawMaterialFormSet(request.POST, prefix='raw_materials')

            if sub_part_formset.is_valid() and raw_material_formset.is_valid():
                product = Product.objects.get(id=product_id)
                sub_parts = []
                for i, form in enumerate(sub_part_formset):
                    sub_part_name = form.cleaned_data.get('name')
                    if sub_part_name:
                        sub_part = SubPart.objects.create(name=sub_part_name)
                        sub_parts.append(sub_part)
                
                product.sub_parts.set(sub_parts)

                for i, form in enumerate(raw_material_formset):
                    raw_material = form.cleaned_data.get('raw_material')
                    quantity_required = form.cleaned_data.get('quantity_required')
                    if raw_material and quantity_required is not None:
                        sub_part = sub_parts[i]  # Use index i to map to sub-part
                        SubPartRawMaterial.objects.create(
                            sub_part=sub_part,
                            raw_material=raw_material,
                            quantity_required=quantity_required
                        )
                
                return redirect('admin_dashboard')
        else:
            sub_part_formset = SubPartFormSet(prefix='sub_parts')
            raw_material_formset = RawMaterialFormSet(prefix='raw_materials')

        return render(request, 'inventory/define_sub_parts.html', {
            'sub_part_formset': sub_part_formset,
            'raw_material_formset': raw_material_formset
        })
    else:
        return redirect('create_product')

@login_required
def check_stock(request):
    raw_materials = RawMaterial.objects.all()
    return render(request, 'inventory/check_stock.html', {'raw_materials': raw_materials})

@login_required
def add_raw_material(request):
    if request.method == 'POST':
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_raw_materials')
    else:
        form = RawMaterialForm()
    return render(request, 'inventory/add_raw_material.html', {'form': form})

@login_required
def view_raw_materials(request):
    raw_materials = RawMaterial.objects.all()
    return render(request, 'inventory/view_raw_materials.html', {'raw_materials': raw_materials})
