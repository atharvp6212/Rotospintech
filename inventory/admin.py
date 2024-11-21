from django.contrib import admin
from .models import RawMaterial, SubPart, Product, SubPartRawMaterial, Color

class SubPartRawMaterialInline(admin.TabularInline):
    model = SubPartRawMaterial
    extra = 1
    fields = ('raw_material', 'quantity_required')


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name',)

@admin.register(SubPart)
class SubPartAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [SubPartRawMaterialInline]  # Add ColorInline here

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_sub_parts', 'get_raw_materials')
    filter_horizontal = ('sub_parts',)

    def get_sub_parts(self, obj):
        return ", ".join([sub_part.name for sub_part in obj.sub_parts.all()])
    get_sub_parts.short_description = 'Sub-Parts'

    def get_raw_materials(self, obj):
        raw_materials = []
        for sub_part in obj.sub_parts.all():
            sub_part_raw_materials = SubPartRawMaterial.objects.filter(sub_part=sub_part)
            for s in sub_part_raw_materials:
                raw_materials.append(f"{sub_part.name}: {s.raw_material.name} ({s.quantity_required})")
        return "; ".join(raw_materials)
    get_raw_materials.short_description = 'Raw Materials'

@admin.register(SubPartRawMaterial)
class SubPartRawMaterialAdmin(admin.ModelAdmin):
    list_display = ('sub_part', 'raw_material', 'quantity_required')
    list_filter = ('sub_part', 'raw_material')
    search_fields = ('sub_part__name', 'raw_material__name')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)