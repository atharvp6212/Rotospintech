from django.contrib import admin
from .models import Order, OrderedSubPart

class OrderedSubPartInline(admin.TabularInline):
    model = OrderedSubPart
    extra = 1  # Number of empty forms to display by default

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date')  # Fields to display in the list view
    search_fields = ('id',)  # Fields to search
    inlines = [OrderedSubPartInline]  # Display ordered sub-parts within the order detail view

admin.site.register(Order, OrderAdmin)
