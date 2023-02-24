import django_filters

from .models import Radiograph


class RadiographFilter(django_filters.FilterSet):
    class Meta:
        model = Radiograph
        fields = ['reading', 'sex', ]