from django.urls import path
from . import views
from evaluacion.views import presentar_examen

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('candidato-panel/', views.panel_candidato, name='panel_candidato'),
    path('logout/', views.logout_view, name='logout'),
    path('examen/', presentar_examen, name='presentar_examen'),
]