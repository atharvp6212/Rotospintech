from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Order, OrderedSubPart
from .forms import OrderForm, OrderedSubPartForm
from django.utils import timezone
from django.contrib import messages
from inventory.models import SubPartRawMaterial, RawMaterial, Color, SubPart,StockHistory
from django.http import JsonResponse

@login_required
def select_sub_part(request):
    sub_parts = SubPart.objects.all()

    if request.method == 'POST':
        selected_sub_part_ids = request.POST.getlist('sub_parts')  # Use getlist for multiple selections

        if selected_sub_part_ids:
            # Join selected IDs with commas and redirect to `enter_new_order` view
            return redirect('enter_new_order', sub_part_ids=','.join(selected_sub_part_ids))

    return render(request, 'orders/select_sub_part.html', {
        'sub_parts': sub_parts,
    })

@login_required
def enter_new_order(request, sub_part_ids):
    sub_part_ids_list = [int(id) for id in sub_part_ids.split(',')]
    selected_sub_parts = SubPart.objects.filter(id__in=sub_part_ids_list)
    order_form = OrderForm(request.POST or None)

    if request.method == 'POST':
        if 'add_sub_part' in request.POST:
            # Handle adding a new sub-part instance
            sub_part_id_to_add = int(request.POST.get('add_sub_part'))
            selected_sub_parts = list(selected_sub_parts) + [SubPart.objects.get(id=sub_part_id_to_add)]
        
        elif 'calculate' in request.POST:
            # Collect order details and redirect to review page
            order_data = []
            for sub_part in selected_sub_parts:
                quantity = int(request.POST.get(f'quantity_{sub_part.id}', 0))
                raw_material_id = int(request.POST.get(f'raw_material_{sub_part.id}', 0))
                if quantity > 0:  # Only include if quantity is greater than zero
                    order_data.append({
                        'sub_part_id': sub_part.id,
                        'quantity': quantity,
                        'raw_material_id': raw_material_id
                    })
            request.session['order_data'] = order_data  # Store order data in session
            return redirect('review_order')  # Redirect to review page
    
    # Prepare descriptions for rendering
    sub_part_descriptions = [
        {
            "name": sub_part.name,
            "raw_materials": [
                {
                    "id": sprm.raw_material.id,
                    "name": sprm.raw_material.name,
                    "quantity_required": sprm.quantity_required,
                    "available_quantity": sprm.raw_material.quantity,
                }
                for sprm in sub_part.subpartrawmaterial_set.all()
            ],
        }
        for sub_part in selected_sub_parts
    ]
    
    return render(request, 'orders/enter_new_order.html', {
        'order_form': order_form,
        'selected_sub_parts': selected_sub_parts,
        'sub_part_descriptions': sub_part_descriptions,
    })
    
@login_required
def review_order(request):
    order_data = request.session.get('order_data')
    required_materials = {}

    if not order_data:
        return redirect('enter_new_order')  # Redirect if no order data in session

    # Calculate required and remaining quantities
    for item in order_data:
        sub_part = SubPart.objects.get(id=item['sub_part_id'])
        raw_material = RawMaterial.objects.get(id=item['raw_material_id'])
        quantity_required = sub_part.subpartrawmaterial_set.get(raw_material=raw_material).quantity_required
        total_quantity_required = item['quantity'] * quantity_required

        if raw_material.id in required_materials:
            required_materials[raw_material.id]['total_quantity_required'] += total_quantity_required
        else:
            required_materials[raw_material.id] = {
                'name': raw_material.name,
                'available_quantity': raw_material.quantity,
                'total_quantity_required': total_quantity_required,
            }

    # Calculate remaining quantities
    for material in required_materials.values():
        material['remaining_quantity'] = material['available_quantity'] - material['total_quantity_required']

    if request.method == 'POST' and 'confirm' in request.POST:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()

            for item in order_data:
                sub_part = SubPart.objects.get(id=item['sub_part_id'])
                raw_material = RawMaterial.objects.get(id=item['raw_material_id'])
                OrderedSubPart.objects.create(
                    order=order,
                    sub_part=sub_part,
                    quantity=item['quantity'],
                    raw_material=raw_material
                )
                total_required_quantity = item['quantity'] * sub_part.subpartrawmaterial_set.get(raw_material=raw_material).quantity_required
                raw_material.quantity -= total_required_quantity
                raw_material.save()

            del request.session['order_data']  # Clear session data
            messages.success(request, "Order placed successfully!")
            return redirect('admin_dashboard')

    return render(request, 'orders/review_order.html', {
        'required_materials': required_materials,
    })

@login_required
def generate_reports(request):
    records = []
    report_title = "Orders Report"  # Default title

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        report_type = request.POST.get('report_type')

        if start_date and end_date:
            try:
                # Parse date strings to datetime objects
                start_date = timezone.make_aware(timezone.datetime.strptime(start_date, '%Y-%m-%d'))
                end_date = timezone.make_aware(timezone.datetime.strptime(end_date, '%Y-%m-%d'))

                if report_type == "stock":
                    # Fetch stock history records within the date range using 'date_added'
                    stock_records = StockHistory.objects.filter(date_added__range=[start_date, end_date])
                    for record in stock_records:
                        records.append({
                            'id': record.id,
                            'date': record.date_added,
                            'details': f"Raw Material: {record.raw_material.name}, Quantity Before: {record.quantity_before}, Quantity Added: {record.quantity_added}, Quantity After: {record.quantity_after}"
                        })
                    report_title = "Stock Report"
                else:
                    # Fetch order records within the date range
                    orders = Order.objects.filter(order_date__range=[start_date, end_date])
                    for order in orders:
                        # Gather details for each order, including raw materials for each sub-part
                        ordered_parts = OrderedSubPart.objects.filter(order=order)
                        details = []
                        for part in ordered_parts:
                            color_name = part.color.name if part.color else 'N/A'
                            raw_material = part.raw_material.name
                            raw_material_weight = part.quantity * part.sub_part.subpartrawmaterial_set.first().quantity_required  # Assume each part has a set quantity
                            sub_part_details = f"{part.sub_part.name} - {part.quantity} units (Color: {color_name})"
                            details.append(f"{sub_part_details} - Raw Material: {raw_material}, Weight: {raw_material_weight}")
                        records.append({
                            'id': order.id,
                            'date': order.order_date,
                            'details': '; '.join(details) or 'No parts ordered'
                        })
                    report_title = "Orders Report"
            except ValueError as e:
                print(f"Date parsing error: {e}")
                records = []

    return render(request, 'orders/generate_reports.html', {
        'records': records,
        'report_title': report_title,
    })