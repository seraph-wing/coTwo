from django.db import models
from django.urls import reverse


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(default = '  ',blank=True)
    net_carbon_emissions = models.FloatField(blank=True,default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('coTwo:production_create', kwargs={'pk': self.pk})


#
#
def get_default_project():
    return Project.objects.get_or_create(name='default')[0].pk
#
# def get_default_project(): return 1
#

class Material(models.Model):
    material_name = models.CharField(max_length=200)
    production_coefficient = models.FloatField(default=0)

    def __str__(self):
        return self.material_name


class MaterialProduction(models.Model):
    # setting the attributes
    KILO = 'KG'
    MCUBE = 'M3'
    MATERIAL_CHOICES = [
        (KILO, 'Kilogrammes'),
        (MCUBE, 'Cubic metres'),
    ]

    # this will go in project
    initial_material_quantity = models.FloatField(default=0)  # m_i in kgs
    material_quantity_unit = models.CharField(max_length=2, choices=MATERIAL_CHOICES, default=KILO)
    # ---------------------------------------------------------------------------------------------------
    # carbon_coefficient = models.FloatField()
    material = models.ForeignKey(to='Material', on_delete=models.CASCADE)
    total_carbon_emission = models.FloatField(blank=True, default=0)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='production',
                                default=get_default_project())

    def __str__(self):
        return self.material.material_name

    def get_absolute_url(self):
        return reverse('coTwo:transport_type_create',kwargs = {'pk':self.project.pk})

    def save(self, *args, **kwargs):
        if self.material_quantity_unit == 'M3':
            self.initial_material_quantity *= 1000
        self.total_carbon_emission = self.material.production_coefficient * self.initial_material_quantity
        super(MaterialProduction, self).save(*args, **kwargs)


class Transport(models.Model):
    transport_name = models.CharField(max_length=200)
    capacity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.transport_name




class MaterialTransportation(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    transport_type = models.ForeignKey('Transport', on_delete=models.CASCADE)
    # this goes in project

    # --------------------------------------------------------------------------
    mileage = models.FloatField()
    fuel_factor = models.FloatField()
    carbon_coefficient = models.FloatField(blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='transport',
                                default=get_default_project())
    # total_carbon_emission = models.FloatField(blank=True, default=0)

    def __str__(self):
        return self.material.material_name

    def save(self, *args, **kwargs):
        self.carbon_coefficient = self.mileage * self.fuel_factor
        # self.total_carbon_emission = self.carbon_coefficient * self.num_trips * self.distance
        super(MaterialTransportation, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('coTwo:transport_create',kwargs = {'pk':self.project.pk})


class ProjectTransportation(models.Model):
    material = models.ForeignKey('MaterialTransportation', on_delete=models.CASCADE)
    num_trips = models.PositiveIntegerField(default=0)
    distance = models.FloatField(default=0)
    total_carbon_emission = models.FloatField(blank=True, default=0)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_transport',
                                default=get_default_project())

    def __str__(self):
        return str(self.material.material.material_name) + str(self.pk)

    def save(self, *args, **kwargs):
        self.total_carbon_emission = self.num_trips * self.distance * self.material.carbon_coefficient
        super(ProjectTransportation, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('coTwo:operation_create', kwargs={'pk': self.project.pk})



class MaterialOperation(models.Model):
    # material = models.ForeignKey('Materials', on_delete=models.CASCADE)
    # this goes in project
    years = models.PositiveIntegerField(default=0)
    electrical_consumption = models.FloatField(default=0)
    # ----------------------------------------------------------------------------------

    electrical_coefficient = models.FloatField(default=0)
    type_of_energy = models.ForeignKey('EnergyType', on_delete=models.CASCADE, default=0)
    total_carbon_coefficient = models.FloatField(default=0)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='operation',
                                default=get_default_project())

    def __str__(self):
        return self.type_of_energy.energy_type

    def save(self, *args, **kwargs):
        self.electrical_coefficient = (self.type_of_energy.percentage / 100) * 0.349
        self.total_carbon_coefficient = self.electrical_coefficient * self.electrical_consumption * self.years
        super(MaterialOperation, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('coTwo:maintenance_create', kwargs={'pk': self.project.pk})



class MaterialMaintenance(models.Model):
    maintenance_materials = models.ForeignKey('Material', on_delete=models.CASCADE)
    material_quantity = models.FloatField()
    lifespan = models.PositiveIntegerField()
    rate_of_repair = models.FloatField()  # in yr^-1
    repair_interval = models.PositiveIntegerField()
    total_emission_coefficient = models.FloatField(default=0)

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='maintenance',
                                default=get_default_project())

    def __str__(self):
        return self.maintenance_materials.material_name

    def save(self, *args, **kwargs):
        self.total_emission_coefficient = self.material_quantity * self.rate_of_repair * \
                                          self.maintenance_materials.production_coefficient * \
                                          (self.lifespan / self.rate_of_repair)
        super(MaterialMaintenance, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('coTwo:project_detail', kwargs={'pk': self.project.pk})



class EnergyType(models.Model):
    energy_type = models.CharField(max_length=200)
    percentage = models.FloatField()

    # change = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.energy_type
