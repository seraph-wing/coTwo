from . import views
from django.urls import path
app_name = 'coTwo'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('project/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/project/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/production/', views.ProductionCreateView.as_view(), name='production_create'),
    path('<int:pk>/transport_type/', views.TransportCreateView.as_view(),name='transport_type_create'),
    path('<int:pk>/transport/', views.ProjectTransportCreateView.as_view(),name='transport_create'),
    path('<int:pk>/operations', views.OperationCreateView.as_view(),name='operation_create'),
    path('<int:pk>/management', views.ManagementCreateView.as_view(),name='maintenance_create'),
    path('projects/all/', views.ProjectListView.as_view(), name='project_list')
]