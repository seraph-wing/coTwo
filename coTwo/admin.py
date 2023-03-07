from django.contrib import admin
from .models import *


# Register your models here.


class MaterialAdmin(admin.ModelAdmin):
    list_display = ['material_name', 'production_coefficient']
    search_fields = ['material_name__material_name']


admin.site.register(Material, MaterialAdmin)


class MaterialProductionAdmin(admin.ModelAdmin):
    fields = ['material', 'initial_material_quantity', 'material_quantity_unit','project']
    list_display = ['material', 'initial_material_quantity', 'total_carbon_emission']
    search_fields = ['material__material_name']


admin.site.register(MaterialProduction, MaterialProductionAdmin)
admin.site.register(Transport)


class MaterialTransportationAdmin(admin.ModelAdmin):
    list_display = ['material', 'transport_type', 'carbon_coefficient']
    search_fields = ['material__material_name', 'transport_type__transport_name']


admin.site.register(MaterialTransportation, MaterialTransportationAdmin)


class ProjectTransportationAdmin(admin.ModelAdmin):
    list_display = ['material', 'total_carbon_emission']


admin.site.register(ProjectTransportation, ProjectTransportationAdmin)


class MaterialOperationAdmin(admin.ModelAdmin):
    fields = ['type_of_energy', 'years', 'electrical_consumption','project']
    list_display = ['type_of_energy', 'years', 'electrical_consumption', 'electrical_coefficient',
                    'total_carbon_coefficient']
    search_fields = ['type_of_energy__energy_type']


admin.site.register(MaterialOperation, MaterialOperationAdmin)


class MaterialMaintenanceAdmin(admin.ModelAdmin):
    fields = ['maintenance_materials', 'material_quantity', 'lifespan', 'rate_of_repair', 'repair_interval','project']
    list_display = ['maintenance_materials', 'material_quantity', 'total_emission_coefficient']
    search_fields = ['maintenance_materials__material_name']


admin.site.register(MaterialMaintenance, MaterialMaintenanceAdmin)
admin.site.register(EnergyType)
admin.site.register(Project)
