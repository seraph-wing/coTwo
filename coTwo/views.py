from django.shortcuts import render

# Create your views here.
from django.views import generic
from . import models
from django.contrib import messages
from django.db.models import Sum
import plotly.express as px
import plotly.offline as plot
import plotly.io as pio
pio.renderers.default = "browser"
class IndexView(generic.base.TemplateView):
    template_name = 'coTwo/index.html'
    # context_object_name = 'latest_question_list'


class ProjectCreateView(generic.CreateView):
    model = models.Project
    template_name = 'coTwo/project_create.html'
    fields = ['name']


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'coTwo/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_material_production'] = models.Project.objects.get(pk=self.kwargs.get('pk')).production.all().aggregate(Sum('total_carbon_emission'))['total_carbon_emission__sum']
        if not context['total_material_production']:
            context['total_material_production'] = 0

        context['total_material_transportation'] = models.Project.objects.get(pk=self.kwargs.get('pk')).project_transport.all().aggregate(Sum('total_carbon_emission'))['total_carbon_emission__sum']
        if not context['total_material_transportation']:
            context['total_material_transportation'] = 0

        context['total_material_operation'] = models.Project.objects.get(pk=self.kwargs.get('pk')).operation.all().aggregate(Sum('total_carbon_coefficient'))['total_carbon_coefficient__sum']
        if not context['total_material_operation']:
            context['total_material_operation'] = 0

        context['total_material_maintenance'] = models.Project.objects.get(pk=self.kwargs.get('pk')).maintenance.all().aggregate(Sum('total_emission_coefficient'))['total_emission_coefficient__sum']
        if not context['total_material_maintenance']:
            context['total_material_maintenance'] = 0
        context['carbon_offset'] = context['total_material_production'] + context['total_material_transportation'] + context['total_material_operation'] + context['total_material_maintenance']
        proj = models.Project.objects.get(pk=self.kwargs.get('pk'))
        proj.net_carbon_emissions = context['carbon_offset']
        x = ['total_material_production','total_material_transportation','total_material_operation','total_material_maintenance']
        labels = ['Material production phase','Material transportation phase','Project Operation phase','Project Maintenance phase']
        y = [context[values] for values in x]
        fig = px.pie(names=labels,values=y,title='Distribution of carbon emission in the project lifecycle')
        context["pie_chart"] = pio.to_html(fig,full_html=False)

        proj.save()

        return context


# Create project listView
class ProjectListView(generic.ListView):
    model = models.Project
    template_name = "coTwo/project_list.html"
    paginate_by = 100


# materials production detail view
# Material production details create
class ProductionCreateView(generic.CreateView):
    model = models.MaterialProduction
    template_name = 'coTwo/production_create.html'
    fields = ['material', 'initial_material_quantity', 'material_quantity_unit']
    context_object_name = 'material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.kwargs.get('pk')
        context['added_materials'] = models.Project.objects.get(pk=self.kwargs.get('pk')).production.all()

        print(context)
        #print(self.get_context_object_name(self))
        return context

    def form_valid(self, form):
        form.instance.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Production data has ben added'
        )
        return super().form_valid(form)


# material transportation details
class TransportCreateView(generic.CreateView):
    model = models.MaterialTransportation
    template_name = 'coTwo/transport_create.html'
    fields = ['material', 'transport_type', 'mileage', 'fuel_factor']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.kwargs.get('pk')
        context['added_transports'] = models.Project.objects.get(pk=self.kwargs.get('pk')).transport.all()

        print(context)
        #print(self.get_context_object_name(self))
        return context
    def form_valid(self, form):
        form.instance.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Transport data has ben added'
        )
        return super().form_valid(form)


class ProjectTransportCreateView(generic.CreateView):
    model = models.ProjectTransportation
    template_name = 'coTwo/project_transport_create.html'
    fields = ['material', 'num_trips', 'distance']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.kwargs.get('pk')
        context['added_transports'] = models.Project.objects.get(pk=self.kwargs.get('pk')).project_transport.all()

        print(context)
        # print(self.get_context_object_name(self))
        return context

    def form_valid(self, form):
        form.instance.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Project Transport data has ben added'
        )
        return super().form_valid(form)


# materials

class OperationCreateView(generic.CreateView):
    model = models.MaterialOperation
    template_name = 'coTwo/operations_create.html'
    fields = ['years', 'electrical_consumption', 'type_of_energy']

    def form_valid(self, form):
        form.instance.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Operations data has ben added'
        )
        return super().form_valid(form)


class ManagementCreateView(generic.CreateView):
    model = models.MaterialMaintenance
    template_name = 'coTwo/maintenance_create.html'
    fields = ['maintenance_materials', 'material_quantity', 'lifespan', 'rate_of_repair', 'repair_interval']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.kwargs.get('pk')
        context['added_materials'] = models.Project.objects.get(pk=self.kwargs.get('pk')).maintenance.all()

        #print(context)
        #print(self.get_context_object_name(self))
        return context

    def form_valid(self, form):
        form.instance.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Maintenance data has ben added'
        )
        return super().form_valid(form)
