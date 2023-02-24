from django.urls import path
from django.views.generic import TemplateView

from .views import RadiographCreateView, RadiographDeleteView, FilteredRadiographListView, RadiographUpdateView, TrainingAnalysisView, DashboardView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("list/", FilteredRadiographListView.as_view(), name="list"),
    path("create/", RadiographCreateView.as_view(), name="create"),
    path("update/<int:pk>/", RadiographUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", RadiographDeleteView.as_view(), name="delete"),
    path("training/", TrainingAnalysisView.as_view(), name="training"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

]